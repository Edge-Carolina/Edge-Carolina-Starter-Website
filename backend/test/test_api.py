import httpx
import pytest

BASE_URL = "http://localhost: 8000"  # Adjust the port if needed

def test_read_main():
    response = httpx.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    user_data = {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "major": "Physics"}
    response = httpx.post(f"{BASE_URL}/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["first_name"] == "John"
