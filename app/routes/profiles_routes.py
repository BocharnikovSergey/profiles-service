from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.profiles_schemas import ProfileCreate, ProfileResponse, ProfileUpdate
from app.db.database import get_async_session
from app.crud.profiles_crud import (
    create_profile,
    get_profile_by_user_id,
    delete_profile_by_user_id,
    update_profile,
)
from app.middlerware.dependency import get_current_user_id

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProfileResponse)
async def create_new_profile(
    payload: ProfileCreate, session: AsyncSession = Depends(get_async_session)
):
    profile = await create_profile(session, payload)
    return profile


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile_api(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    profile = await get_profile_by_user_id(session, user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
):
    profile = await get_profile_by_user_id(session, int(user_id))

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.patch("/me", response_model=ProfileResponse)
async def update_my_profile(
    payload: ProfileUpdate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
):
    updated_profile = await update_profile(session, int(user_id), payload)

    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return updated_profile


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile_route(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    deleted = await delete_profile_by_user_id(session, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Profile not found")

    return None
