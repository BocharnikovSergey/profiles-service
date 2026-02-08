from conftest import client
import pytest

@pytest.mark.asyncio
async def test_register_user_success(client):
    payload = {
        "email": "newuser@example.com",
        "password": "very-secret"
    }
    response = await client.post("api/user/create",json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"



@pytest.mark.asyncio
async def test_get_user_success(client):

    email = "testemail@example.com"
    payload = {
        "email": email,
        "password": "1234"
    }
    response = await client.post("api/user/create",json=payload)
    user_data = response.json()
    user_id = user_data["id"]

    response = await client.get(f"api/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == email


@pytest.mark.asyncio
async def test_create_and_delete_user(client):
    payload = {"email": "uuid_test@example.com", "password": "pass"}
    create_res = await client.post("/api/user/create", json=payload)
    assert create_res.status_code == 201
    
    user_data = create_res.json()
    user_id = user_data["id"]
    
    get_res = await client.get(f"/api/user/{user_id}")
    assert get_res.status_code == 200
    
    del_res = await client.delete(f"/api/user/{user_id}")
    assert del_res.status_code == 204
