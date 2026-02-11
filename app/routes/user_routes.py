from fastapi import APIRouter,status,Depends,HTTPException
from app.schemas.users_schemas import UserCreate,UserResponse,UserUpdate
from app.db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user_crud import create_user,get_user,delete_user,update_user
from app.middlerware.dependency import get_current_user_id
router = APIRouter(tags=["Users"])

@router.post("/api/user/create",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def api_create_user(payload:UserCreate,session: AsyncSession = Depends(get_async_session)):
    user = await create_user(session,payload)
    return user

@router.get("/api/user/{user_id}",status_code=status.HTTP_200_OK,response_model=UserResponse)
async def api_get_user(user_id: int,session: AsyncSession = Depends(get_async_session)):
    user = await get_user(session,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.get("/api/users/me", response_model=UserResponse)
async def read_users_me(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid User ID format from Gateway")

    user = await get_user(session, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/api/users/me", response_model=UserResponse)
async def update_user_me(
    payload: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    id = int(user_id)
    updated_user = await update_user(session, id, payload) 
    return updated_user

@router.delete("/api/user/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_user(user_id:int,session: AsyncSession = Depends(get_async_session)):
    user = await delete_user(session,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    

    