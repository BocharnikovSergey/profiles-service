from fastapi import HTTPException, status
from redis.asyncio import Redis

from app.crud.profiles_crud import get_profile_id_by_user_id
from app.db.database import AsyncSessionLocal
from config import settings


async def get_profile_id(user_id: int, redis_client: Redis) -> int:
    key = f"profile_id:{user_id}"
    cached_profile_id = await redis_client.get(key)

    if cached_profile_id is not None:
        return int(cached_profile_id)

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
    await redis_client.set(
        key,
        profile_id,
        ex=settings.redis_ttl,
    )
    return profile_id
