from fastapi import Header, HTTPException, status
from typing import Annotated

async def get_current_user_id(
    x_user_id: Annotated[str | None, Header()] = None
) -> str:
    """
    Достает ID пользователя из заголовка, который проставил API Gateway.
    Если заголовка нет — значит запрос прошел мимо Gateway (это опасно).
    """
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-Id header is missing. Direct access not allowed."
        )
    return x_user_id