from pydantic import BaseModel



class UserCreate(BaseModel):
    email: str
    password: str

class UserDelete(BaseModel):
    email: str
    password: str
