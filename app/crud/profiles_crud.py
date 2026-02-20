from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Profile
from sqlalchemy import update
from app.db.models import Profile
from app.schemas.profiles_schemas import ProfileCreate, ProfileResponse, ProfileUpdate


async def create_profile(db: AsyncSession, profile_in: ProfileCreate) -> Profile:

    new_profile = Profile(
        user_id=profile_in.user_id,
        first_name=profile_in.first_name,
        last_name=profile_in.last_name,
        phone_number=profile_in.phone_number,
        avatar_url=profile_in.avatar_url,
    )

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
