from fastapi import APIRouter,status,Depends,HTTPException
from app.schemas.users_schemas import UserCreate,UserResponse
from app.db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user_crud import create_user,get_user,delete_user
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
@router.delete("/api/user/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_user(user_id:int,session: AsyncSession = Depends(get_async_session)):
    user = await delete_user(session,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    

    