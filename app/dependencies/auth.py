import logging

from fastapi import HTTPException, Request, status

logger = logging.getLogger(__name__)


def get_current_id(request: Request, key: str) -> int:
    user = getattr(request.state, "user", None)
    if not isinstance(user, dict):
        logger.warning(
            f"request.state.user Не является словарем. Type: {type(user)}. data: {user}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    id = user.get(key)
    logger.info("ID пользователя %s", id)
    if id in (None, ""):
        logger.warning(f"sub отсутствует в user_data. Type {type(user)}. data: {user}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    try:
        return int(id)
    except (TypeError, ValueError) as exc:
        logger.exception(f"Значение {id} не удалось преобразовать в int. data: {id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from exc


def get_current_user_id(request: Request) -> int:
    return get_current_id(request, "id")


def get_current_profile_id(request: Request) -> int:
    return get_current_id(request, "profile_id")


def check_user_access(request: Request, user_id: int) -> int:
    current_user_id = get_current_user_id(request)

    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    return current_user_id
