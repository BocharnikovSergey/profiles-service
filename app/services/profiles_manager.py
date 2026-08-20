from typing import TypeVar

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.profiles_crud import (
    create_profile as crud_create_profile,
    admin_create_profile as crud_admin_create_profile,
    delete_profile_by_user_id as crud_delete_profile_by_user_id,
    delete_profile_by_id as crud_delete_profile_by_id,
    get_profile_by_user_id as crud_get_profile_by_user_id,
    get_profile_by_id as crud_get_profile_by_id,
    update_profile_by_user_id as crud_update_profile_by_user_id,
    update_profile_by_id as crud_update_profile_by_id,
)
from app.crud.favorite_locations_crud import (
    add_favorite_location as crud_add_favorite_location,
    delete_favorite_location as crud_delete_favorite_location,
    get_favorite_location as crud_get_favorite_location,
    get_favorite_location_ids as crud_get_favorite_location_ids,
)
from app.schemas.admin_schemas import ProfileCreate as AdminProfileCreate
from app.schemas.profiles_schemas import (
    ProfileCreate, ProfileUpdate
)


T = TypeVar("T")


class ProfileManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_profile(self, user_id: int, profile_in: ProfileCreate):
        existing_profile = await crud_get_profile_by_user_id(self.db, user_id)
        self._raise_conflict_if_exists(existing_profile)

        return await crud_create_profile(self.db, user_id, profile_in)

    async def admin_create_profile(self, profile_in: AdminProfileCreate):
        existing_profile = await crud_get_profile_by_user_id(
            self.db, profile_in.user_id
        )
        self._raise_conflict_if_exists(existing_profile)

        return await crud_admin_create_profile(self.db, profile_in)

    async def get_profile_by_user_id(self, user_id: int):
        profile = await crud_get_profile_by_user_id(self.db, user_id)
        self._raise_not_found(profile)
        return profile

    async def get_profile_by_id(self, profile_id: int):
        profile = await crud_get_profile_by_id(self.db, profile_id)
        self._raise_not_found(profile)
        return profile

    async def update_profile_by_user_id(self, user_id: int, payload: ProfileUpdate):
        profile = await crud_update_profile_by_user_id(self.db, user_id, payload)
        self._raise_not_found(profile)
        return profile

    async def update_profile_by_id(self, profile_id: int, payload: ProfileUpdate):
        profile = await crud_update_profile_by_id(self.db, profile_id, payload)
        self._raise_not_found(profile)
        return profile

    async def delete_profile_by_user_id(self, user_id: int) -> None:
        deleted = await crud_delete_profile_by_user_id(self.db, user_id)
        self._raise_not_found(deleted)

    async def delete_profile_by_id(self, profile_id: int) -> None:
        deleted = await crud_delete_profile_by_id(self.db, profile_id)
        self._raise_not_found(deleted)


    async def add_favorite_location(self, user_id: int, location_id: int):
        profile = self._raise_not_found(
            await crud_get_profile_by_user_id(self.db, user_id)
        )
        self._raise_conflict_if_exists(
            await crud_get_favorite_location(self.db, profile.id, location_id),
            detail="Location is already in favorites"
        )
        return await crud_add_favorite_location(
            self.db, profile.id, location_id,
        )

    async def get_favorite_location_ids(
        self, user_id: int,
    ) -> list[int]:
        profile = self._raise_not_found(
            await crud_get_profile_by_user_id(self.db, user_id)
        )
        return await crud_get_favorite_location_ids(self.db, profile.id)

    async def delete_favorite_location(
        self, user_id: int, location_id: int,
    ) -> None:
        profile = self._raise_not_found(
            await crud_get_profile_by_user_id(self.db, user_id)
        )
        self._raise_not_found(
            await crud_delete_favorite_location(
                self.db, profile.id, location_id,
            ), detail="Favorite location not found"
        )


    @staticmethod
    def _raise_not_found(obj: T | None, detail="Profile not found") -> T:
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return obj

    @staticmethod
    def _raise_conflict_if_exists(
        existing_obj, detail="Profile already exists"
    ):
        if existing_obj:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=detail,
            )
