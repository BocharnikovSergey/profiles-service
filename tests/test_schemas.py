from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.schemas.admin_schemas import ProfileCreate as AdminProfileCreate
from app.schemas.admin_schemas import ProfileUpdate as AdminProfileUpdate
from app.schemas.profiles_schemas import ProfileResponse


@pytest.fixture(
    params=[
        (
            AdminProfileCreate,
            {"user_id": 7, "first_name": "Ann"},
        ),
        (
            AdminProfileUpdate,
            {"first_name": "Ann"},
        ),
    ]
)
def profile_schema(request):
    return request.param


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


@pytest.mark.parametrize(
    ("phone_number", "expected"),
    [
        ("+7 (918) 999-99-99", "+79189999999"),
        ("+7 777 123 45 67", "+77771234567"),
        ("+7 (918) 8888888", "+79188888888")
    ],
)
def test_profile_phone_number_is_normalized(
    profile_schema, phone_number, expected
):
    schema, data = profile_schema
    profile = schema(**data, phone_number=phone_number)
    assert profile.phone_number == expected


@pytest.mark.parametrize(
    "phone_number",
    ["12345", "abcdef", "+799912345", "+799912345678901", "+7", "   "],
)
def test_profile_rejects_invalid_phone_number(profile_schema, phone_number):
    schema, data = profile_schema
    with pytest.raises(ValidationError):
        schema(**data, phone_number=phone_number)


def test_profile_phone_number_can_be_none(profile_schema):
    schema, data = profile_schema
    profile = schema(**data, phone_number=None)
    assert profile.phone_number is None
