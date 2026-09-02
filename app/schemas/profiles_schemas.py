from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .validators.phone_number import normalize_phone_number

MIN_LEN_NAME = 2
MAX_LEN_NAME = 15
PATTERN_NAME = r"^[A-Za-zА-Яа-яЁё]+(?:[ -][A-Za-zА-Яа-яЁё]+)?$"
MAX_LEN_ABOUT_ME = 300


class ProfileBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=15,
        pattern=PATTERN_NAME,
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=15,
        pattern=PATTERN_NAME,
    )
    phone_number: str | None = None
    age: int | None = None
    about_me: str | None = Field(
        default=None,
        max_length=MAX_LEN_ABOUT_ME,
        description="Произвольная информация о себе.",
    )
    activities: list[str] = Field(
        default_factory=list,
        description="External activity identifiers from activities service",
    )
    country: str | None = None
    city: str | None = None
    citizenship: str | None = None
    currency: str | None = None
    # Времено отключено по просьбе тестеров. До подключения бакета
    # avatar_url: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, phone_number: str | None) -> str | None:
        if phone_number is not None:
            return normalize_phone_number(phone_number)
        return None


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
    created_at: datetime


class FavoriteLocationsResponse(BaseModel):
    location_ids: list[FavoriteLocationResponse]
