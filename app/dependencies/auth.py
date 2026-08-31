import logging

from fastapi import HTTPException, Request, status

from app.utils.converters import convert_value_to_int
from app.utils.validators import require_or_unauthorized

logger = logging.getLogger(__name__)


def _get_current_id_form_state(request: Request, key: str) -> int:
    user = getattr(request.state, "user", None)
    if not isinstance(user, dict):
        logger.warning(
            f"request.state.user Не является словарем. Type: {type(user)}. data: {user}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    current_id = user.get(key)
    logger.info("ID пользователя %s", id)
    if current_id in (None, ""):
        logger.warning(f"sub отсутствует в user_data. Type {type(user)}. data: {user}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return require_or_unauthorized(convert_value_to_int(current_id))


def get_current_user_id(request: Request) -> int:
    return _get_current_id_form_state(request, "id")


def get_current_profile_id(request: Request) -> int:
    return _get_current_id_form_state(request, "profile_id")


def check_user_access(request: Request, user_id: int) -> int:
    current_user_id = get_current_user_id(request)

    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return current_user_id
