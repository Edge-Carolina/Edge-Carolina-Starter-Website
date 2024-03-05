import pytest
from ...services.join import JoinService
from ...entities.user_entity import UserEntity
from ...models.user_data import UserData
from ...services.exceptions import (
    ResourceNotFoundException,
    UserRegistrationException,
)
from .fixtures import join_service
from ..user_data import fake_data_fixture


def test_get_users(join_service: JoinService) -> None:
    users = join_service.get_users()
    assert len(users) == 1  # Assuming you have only one user in your mock data

def test_get_user(join_service: JoinService) -> None:
    user_id = 1
    user = join_service.get_user(user_id)
    assert user.id == user_id
    assert user.first_name == "user"
    assert user.last_name == "user"
    assert user.email == "root@unc.edu"
    assert user.major == "math"

def test_create_user(join_service: JoinService) -> None:
    user_data = UserData(id=2, first_name="Jane", last_name="Doe", email="jane.doe@example.com", major="Physics")
    created_user = join_service.create_user(user_data)
    assert created_user.email == user_data.email

def test_create_user_existing_email(join_service: JoinService) -> None:
    user_data = UserData(id=2, first_name="John", last_name="Doe", email="root@unc.edu", major="Physics")
    with pytest.raises(UserRegistrationException):
        join_service.create_user(user_data)

def test_update_user(join_service: JoinService) -> None:
    updated_data = UserData(id=1, first_name="Updated", last_name="User", email="root@unc.edu", major="Updated Major")
    join_service.update_user(updated_data)
    updated_user = join_service.get_user(1)
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "User"
    assert updated_user.major == "Updated Major"

def test_delete_user(join_service: JoinService) -> None:
    join_service.delete_user(1)
    with pytest.raises(ResourceNotFoundException):
        join_service.get_user(1)

def test_get_user_by_id(join_service: JoinService) -> None:
    user = join_service.get_user(1)
    assert user.id == 1
    assert user.first_name == "user"
    assert user.last_name == "user"
    assert user.email == "root@unc.edu"
    assert user.major == "math"

def test_get_user_by_id_not_found(join_service: JoinService) -> None:
    with pytest.raises(ResourceNotFoundException):
        join_service.get_user(999)

def test_check_email_registered(join_service: JoinService) -> None:
    assert join_service.check_email_registered("root@unc.edu") is True
    assert join_service.check_email_registered("nonexistent@example.com") is False
