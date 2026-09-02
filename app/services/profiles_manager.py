from typing import TypeVar

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.locations_client import check_location_exists
from app.crud.favorite_locations_crud import (
    delete_favorite_location as crud_delete_favorite_location,
)
from app.crud.favorite_locations_crud import (
    get_favorite_location_ids as crud_get_favorite_location_ids,
)
from app.crud.favorite_locations_crud import (
    get_or_create_favorite_location as crud_get_or_create_favorite_location,
)
from app.crud.profiles_crud import (
    admin_create_profile as crud_admin_create_profile,
)
from app.crud.profiles_crud import (
    create_profile as crud_create_profile,
)
from app.crud.profiles_crud import (
    delete_profile_by_id as crud_delete_profile_by_id,
)
from app.crud.profiles_crud import (
    delete_profile_by_user_id as crud_delete_profile_by_user_id,
)
from app.crud.profiles_crud import (
    get_profile_by_id as crud_get_profile_by_id,
)
from app.crud.profiles_crud import (
    get_profile_by_user_id as crud_get_profile_by_user_id,
)
from app.crud.profiles_crud import (
    update_profile_by_id as crud_update_profile_by_id,
)
from app.crud.profiles_crud import (
    update_profile_by_user_id as crud_update_profile_by_user_id,
)
from app.schemas.admin_schemas import ProfileCreate as AdminProfileCreate
from app.schemas.profiles_schemas import ProfileCreate, ProfileUpdate
from app.db.models import FavoriteLocation

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
        await check_location_exists(location_id)
        favorite_location = await crud_get_or_create_favorite_location(
            self.db,
            user_id,
            location_id,
        )
        self._raise_not_found(favorite_location, detail="Not found")
        return favorite_location

    async def get_favorite_location_ids(
        self,
        user_id: int,
    ) -> list[FavoriteLocation]:
        return await crud_get_favorite_location_ids(self.db, user_id)

    async def delete_favorite_location(
        self,
        user_id: int,
        location_id: int,
    ) -> None:
        await crud_delete_favorite_location(self.db, user_id, location_id)

    def get_or_raise_not_found(self, obj: T, detail: str = "Profile not found") -> T:
        self._raise_not_found(obj, detail)
        return obj

    @staticmethod
    def _raise_not_found(obj: T, detail: str = "Profile not found") -> None:
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    @staticmethod
    def _raise_conflict_if_exists(
        existing_obj: T | None, detail: str = "Profile already exists"
    ) -> None:
        if existing_obj:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )
