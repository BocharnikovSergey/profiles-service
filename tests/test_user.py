from conftest import client


def test_register_user_success(client):
    payload = {
        "email": "newuser@example.com",
        "password": "very-secret"
    }
    response = client.post("api/user/create",json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"

def test_get_user_success(client):
    email = "testemail@example.com"
    response = client.get(f"api/user/{email}")
    assert response.status_code == 200
    assert response.json()["email"] == email

def test_delete_user_success(client):
    payload = {"email": "testemail@example.com","password":"pass123"}
    response = client.delete("api/user/delete",json=payload)
    assert response.status_code == 204
    response_2 = client.get(f"api/user/{payload.email}")
    assert response_2.status_code == 404
