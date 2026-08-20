from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import FavoriteLocation


async def _create_favorite_location(
    db: AsyncSession, favorite_location: FavoriteLocation,
) -> FavoriteLocation:
    db.add(favorite_location)
    await db.commit()
    await db.refresh(favorite_location)

    return favorite_location


async def _find_favorite_location(
    db: AsyncSession, profile_id: int, location_id: int,
) -> FavoriteLocation | None:
    return (
        await db.execute(
            select(FavoriteLocation).where(
                FavoriteLocation.profile_id == profile_id,
                FavoriteLocation.location_id == location_id,
                )
            )
        ).scalar_one_or_none()


async def _find_favorite_location_ids(
    db: AsyncSession, profile_id: int,
) -> list[int]:
    return list((
        await db.execute(
            select(FavoriteLocation.location_id).where(
                FavoriteLocation.profile_id == profile_id
                ).order_by(FavoriteLocation.created_at)
        )
    ).scalars().all())


async def _delete_favorite_location(
    db: AsyncSession, favorite_location: FavoriteLocation | None,
) -> bool:
    if not favorite_location :
        return False

    await db.delete(favorite_location)
    await db.commit()
    return True


async def add_favorite_location(
    db: AsyncSession, profile_id: int, location_id: int,
) -> FavoriteLocation:
    return await _create_favorite_location(
        db, FavoriteLocation(profile_id=profile_id,location_id=location_id)
    )


async def get_favorite_location(
    db: AsyncSession, profile_id: int, location_id: int,
) -> FavoriteLocation | None:
    return await _find_favorite_location(db, profile_id, location_id)


async def get_favorite_location_ids(
    db: AsyncSession, profile_id: int
) -> list[int]:
    return await _find_favorite_location_ids(db, profile_id)


async def delete_favorite_location(
    db: AsyncSession, profile_id: int, location_id: int,
) -> bool:
    return await _delete_favorite_location(
        db, await _find_favorite_location(db, profile_id, location_id)
    )
