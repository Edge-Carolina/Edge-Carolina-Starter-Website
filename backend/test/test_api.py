import httpx
import pytest
from backend.models.user_data import UserData
from backend.services.join import JoinService
from .services.conftest import session, test_engine, reset_database
from sqlalchemy.orm import Session
from .user_data import fake_data_fixture



BASE_URL = "http://localhost:8000"  # Adjust the port if needed

@pytest.fixture(scope="function")
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client

def test_get_users(client: httpx.Client, session: Session):
    # Insert a user into the database
    user = UserData(id=1, first_name="Test", last_name="User", email="test@example.com", major="Computer Science")
    session.add(user)
    session.commit()

    response = client.get("/api/join")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['first_name'] == "Test"

def test_get_user(client: httpx.Client, session: Session):
    # Insert a user into the database
    user = UserData(id=2, first_name="Test", last_name="User", email="test@example.com", major="Computer Science")
    session.add(user)
    session.commit()

    response = client.get(f"/api/join/{user.id}")
    assert response.status_code == 200
    assert response.json()['first_name'] == "Test"

def test_create_user(client: httpx.Client):
    user_data = {"id": 3, "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "major": "Physics"}
    response = client.post("/api/join", json=user_data)
    assert response.status_code == 201
    assert response.json()['first_name'] == "John"

def test_update_user(client: httpx.Client, session: Session):
    # Insert a user into the database
    user = UserData(id=4, first_name="Test", last_name="User", email="test@example.com", major="Computer Science")
    session.add(user)
    session.commit()

    updated_user_data = {"id": user.id, "first_name": "Updated", "last_name": "User", "email": "updated@example.com", "major": "Math"}
    response = client.put("/api/join", json=updated_user_data)
    assert response.status_code == 200
    assert response.json()['first_name'] == "Updated"

def test_delete_user(client: httpx.Client, session: Session):
    # Insert a user into the database
    user = UserData(id=5, first_name="Test", last_name="User", email="test@example.com", major="Computer Science")
    session.add(user)
    session.commit()

    response = client.delete(f"/api/join/{user.id}")
    assert response.status_code == 200

def test_check_email_registered(client: httpx.Client, session: Session):
    # Insert a user into the database
    user = UserData(id=6, first_name="Test", last_name="User", email="test@example.com", major="Computer Science")
    session.add(user)
    session.commit()

    response = client.get(f"/api/join/check-email/{user.email}")
    assert response.status_code == 200
    assert response.json() is True

    response = client.get("/api/join/check-email/nonexistent@example.com")
    assert response.status_code == 200
    assert response.json() is False