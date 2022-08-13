import pytest
from jose import jwt

from app import schemas
from app.oauth2 import SECRET_KEY, ALGORITHM


def test_create_user(client):
    res = client.post('/users/', json={"email": "hello@example.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@example.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    pk: str = payload.get("user_id")
    assert pk == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrong@example.com", "password123", 403),
    ("hello@example.com", "password", 403),
    (None, "password123", 422),
    ("hello@example.com", None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})
    assert res.status_code == status_code

