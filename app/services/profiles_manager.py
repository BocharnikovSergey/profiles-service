from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.profiles_crud import (
    create_profile as crud_create_profile,
    delete_profile_by_user_id as crud_delete_profile_by_user_id,
    get_profile_by_user_id as crud_get_profile_by_user_id,
    update_profile as crud_update_profile,
)
from app.schemas.profiles_schemas import ProfileCreate, ProfileUpdate


class ProfileManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_profile(self, user_id: int, profile_in: ProfileCreate):
        existing_profile = await crud_get_profile_by_user_id(self.db, user_id)
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Profile already exists",
            )

        return await crud_create_profile(self.db, user_id, profile_in)

    async def get_profile_by_user_id(self, user_id: int):
        profile = await crud_get_profile_by_user_id(self.db, user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        return profile

    async def update_profile(self, user_id: int, payload: ProfileUpdate):
        profile = await crud_update_profile(self.db, user_id, payload)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        return profile

    async def delete_profile_by_user_id(self, user_id: int) -> None:
        deleted = await crud_delete_profile_by_user_id(self.db, user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
