from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Profile
from app.schemas.profiles_schemas import ProfileCreate, ProfileUpdate


async def create_profile(
    db: AsyncSession, user_id: int, profile_in: ProfileCreate
) -> Profile:
    profile_data = profile_in.model_dump(exclude_unset=True)
    new_profile = Profile(user_id=user_id, **profile_data)

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    return new_profile


async def get_profile_by_user_id(db: AsyncSession, user_id: int) -> Profile | None:

    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    return result.scalar_one_or_none()


async def delete_profile_by_user_id(db: AsyncSession, user_id: int) -> bool:
    """
    Удаляет профиль по user_id.
    Возвращает True если удален, иначе False.
    """

    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()

    if not profile:
        return False

    await db.delete(profile)
    await db.commit()

    return True


async def update_profile(
    db: AsyncSession, user_id: int, payload: ProfileUpdate
) -> Profile | None:

    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()

    if not profile:
        return None

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)

    return profile
