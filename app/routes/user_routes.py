from fastapi import APIRouter,status
from app.schemas.users_schemas import UserCreate,UserDelete
router = APIRouter(tags=["Users"])

@router.post("/api/user/create",status_code=status.HTTP_201_CREATED)
async def create_user(payload:UserCreate):
    return {"email": payload.email}

@router.get("/api/user/{email}",status_code=status.HTTP_200_OK)
async def get_user(email: str):
    return {"email": email}
@router.delete("/api/user/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(payload:UserDelete):
    return payload