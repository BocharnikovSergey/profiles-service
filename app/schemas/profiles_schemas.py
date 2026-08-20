from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from pydantic import Field


class ProfileBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
    # Времено отключено по просьбе тестеров. До подключения бакета
    # avatar_url: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    role: str
    created_at: datetime
    updated_at: datetime


class FavoriteLocationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    location_id: int = Field(gt=0)


class FavoriteLocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    location_id: int

class FavoriteLocationsResponse(BaseModel):

    location_ids: list[int]
