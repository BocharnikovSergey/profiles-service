from pydantic import BaseModel,EmailStr
from typing import Optional 



class UserCreate(BaseModel):
    email: str
    password: str
class UserResponse(BaseModel):
   id: int
   email: str
   class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None 
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
