from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import Field


class ProfileBase(BaseModel):
    user_id: Optional[int] = Field(gt=0)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None
    about_me: Optional[str] = None
    activities: list[str] = Field(
        default_factory=list,
        description="External activity identifiers from activities service",
    )
    country: Optional[str] = None
    city: Optional[str] = None
    citizenship: Optional[str] = None
    currency: Optional[str] = None
    avatar_url: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    role: str
    created_at: datetime
    updated_at: datetime
