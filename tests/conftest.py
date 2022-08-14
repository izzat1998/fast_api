import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import get_db, Base
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}' \
                          f'@{settings.database_hostname}' \
                          f':{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user_2(client):
    user_data = {'email': 'test1@example.com',
                 'password': 'password123'}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def test_user(client):
    user_data = {'email': 'test@example.com',
                 'password': 'password123'}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user_2):
    posts_data = [
        {"title": "Post 1", "content": "Post 1", "owner_id": test_user["id"]},
        {"title": "Post 2", "content": "Post 2", "owner_id": test_user["id"]},
        {"title": "Post 3", "content": "Post 3", "owner_id": test_user["id"]},
        {"title": "Post 4", "content": "Post 4", "owner_id": test_user_2["id"]},
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
