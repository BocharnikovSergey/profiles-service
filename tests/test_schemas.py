from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.schemas.admin_schemas import ProfileCreate as AdminProfileCreate
from app.schemas.admin_schemas import ProfileUpdate as AdminProfileUpdate
from app.schemas.profiles_schemas import ProfileResponse
from app.schemas.profiles_schemas import (
    FavoriteLocationCreate, FavoriteLocationResponse, FavoriteLocationsResponse,
)


def make_profile(**overrides):
    profile = {
        "id": 1,
        "user_id": 7,
        "role": "user",
        "first_name": "Ann",
        "last_name": None,
        "phone_number": None,
        "age": None,
        "about_me": None,
        "activities": [],
        "country": None,
        "city": None,
        "citizenship": None,
        "currency": None,
        "created_at": datetime(2024, 1, 1, tzinfo=UTC),
        "updated_at": datetime(2024, 1, 1, tzinfo=UTC),
    }
    profile.update(overrides)
    return profile


def test_profile_response_accepts_orm_attributes():
    profile = SimpleNamespace(**make_profile(first_name="Ann"))

    response = ProfileResponse.model_validate(profile)

    assert response.id == 1
    assert response.user_id == 7
    assert response.first_name == "Ann"


def test_admin_profile_create_requires_positive_user_id():
    with pytest.raises(ValidationError):
        AdminProfileCreate(first_name="Ann")

    with pytest.raises(ValidationError):
        AdminProfileCreate(user_id=0, first_name="Ann")

    assert AdminProfileCreate(user_id=7, first_name="Ann").user_id == 7


def test_admin_profile_update_rejects_user_id():
    with pytest.raises(ValidationError):
        AdminProfileUpdate(user_id=8, first_name="Ann")


def test_favorite_location_create_accepts_positive_location_id():
    favorite_location = FavoriteLocationCreate(location_id=10)
    assert favorite_location.location_id == 10


@pytest.mark.parametrize("location_id", [0, -1, -10])
def test_favorite_location_create_rejects_non_positive_location_id(
    location_id,
):
    with pytest.raises(ValidationError):
        FavoriteLocationCreate(location_id=location_id)


def test_favorite_location_create_rejects_extra_fields():
    with pytest.raises(ValidationError):
        FavoriteLocationCreate(location_id=10, profile_id=1)


def test_favorite_location_response_accepts_orm_attributes():
    favorite_location = SimpleNamespace(
        location_id=10, created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    response = FavoriteLocationResponse.model_validate(
        favorite_location
    )
    assert response.location_id == 10
    assert response.created_at == datetime(2024, 1, 1, tzinfo=timezone.utc)


def test_favorite_locations_response_accepts_favorite_locations():
    response = FavoriteLocationsResponse(
        location_ids=[
            FavoriteLocationResponse(
                location_id=10,
                created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            ),
            FavoriteLocationResponse(
                location_id=20,
                created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
            ),
        ]
    )
    assert len(response.location_ids) == 2
    assert response.location_ids[0].location_id == 10
    assert response.location_ids[1].location_id == 20


def test_favorite_locations_response_accepts_empty_list():
    response = FavoriteLocationsResponse(location_ids=[])
    assert response.location_ids == []