import base64
import json
from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi import status


class StubProfileManager:
    def __init__(self):
        self.calls = []
        self.profile = {
            "id": 1,
            "user_id": 7,
            "role": "user",
            "first_name": "Ann",
            "last_name": "Smith",
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

    async def get_profile_by_user_id(self, user_id):
        self.calls.append(("get_profile_by_user_id", user_id))
        return self.profile


@pytest.mark.asyncio
async def test_x_user_claims_header_is_restored_into_request_state(
    client, override_manager, monkeypatch
):
    manager = override_manager(StubProfileManager())

    async def mock_get_profile_id(user_id: int, redis_client: Any) -> int:
        assert user_id == 7
        return 1

    monkeypatch.setattr(
        "app.middlerware.request_context.get_profile_id",
        mock_get_profile_id,
    )

    claims = base64.urlsafe_b64encode(json.dumps({"id": "7"}).encode("utf-8")).decode(
        "ascii"
    )

    response = await client.get(
        "/api/profile/me",
        headers={"X-User-Claims": claims},
    )

    assert response.status_code == status.HTTP_200_OK
    assert manager.calls == [("get_profile_by_user_id", 7)]
