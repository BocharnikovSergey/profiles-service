import logging
from typing import Any

from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def convert_value_to_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        logger.exception(f"Значение не удалось преобразовать в int. data: {value}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from exc
