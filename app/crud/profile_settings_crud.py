from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import ProfileSettings
from app.schemas.profiles_schemas import ProfileSettingsUpdate

from .utils import _update


async def _find_settings_by_profile(
    db: AsyncSession, profile_id: int
) -> ProfileSettings | None:
    return (
        await db.execute(
            select(ProfileSettings).where(ProfileSettings.profile_id == profile_id)
        )
    ).scalar_one_or_none()


async def get_profile_settings(
    db: AsyncSession,
    profile_id: int,
) -> ProfileSettings | None:
    return await _find_settings_by_profile(db, profile_id)


async def update_profile_settings(
    db: AsyncSession,
    settings: ProfileSettings,
    payload: ProfileSettingsUpdate,
) -> ProfileSettings:
    return await _update(db, settings, payload)
