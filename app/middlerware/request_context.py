import base64
import json
import logging

from fastapi import HTTPException, Request, status

from app.crud.profiles_crud import get_profile_id_by_user_id
from app.db.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


def _urlsafe_b64decode_padded(value: str) -> bytes:
    padded = value + "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii"))


async def user_context_middleware(request: Request, call_next):
    """
    Восстанавливает request.state.user из заголовков, которые проставляет gateway.

    Ожидаемые заголовки:
    - X-User-Claims: base64url(JSON) с claims пользователя
    - X-User-ID: fallback, если нужен только идентификатор
    """
    logger.info("Middleware start")
    if getattr(request.state, "user", None) is None:
        claims_header = request.headers.get("x-user-claims")
        user_id_header = request.headers.get("x-user-id")

        if claims_header:
            try:
                raw = _urlsafe_b64decode_padded(claims_header)
                user = json.loads(raw.decode("utf-8"))

                if not isinstance(user, dict):
                    raise TypeError("X-User-Claims must be a JSON object")
                request.state.user = user
            except Exception:
                logger.warning("Invalid X-User-Claims header", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                )
            logger.info("Middleware user=%r", getattr(request.state, "user", None))
        elif user_id_header:
            try:
                user_id = int(user_id_header)
            except (TypeError, ValueError) as exc:
                logger.exception(
                    f"Значение user_id не удалось преобразовать в int. data: {user_id}"
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                ) from exc

            async with AsyncSessionLocal() as session:
                profile_id = await get_profile_id_by_user_id(
                    user_id=user_id,
                    db=session,
                )
            if profile_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                )
            request.state.user = {"id": user_id_header, "profile_id": profile_id}

    response = await call_next(request)
    logger.info("Middleware end")
    return response
