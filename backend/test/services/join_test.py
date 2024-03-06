import pytest
from ...services.join import JoinService
from ...entities.user_entity import UserEntity
from ...models.user_data import UserData
from ...services.exceptions import (
    ResourceNotFoundException,
    UserRegistrationException,
)
from .fixtures import join_service
from ..user_data import fake_data_fixture, root, updated_root, user


def test_get_users(join_service: JoinService) -> None:
    users = join_service.get_users()
    assert len(users) == 1 
    
def test_get_user(join_service: JoinService) -> None:
    user_id = 1
    user = join_service.get_user(user_id)
    assert user.id == user_id
    assert user.first_name == "root"
    assert user.last_name == "root"
    assert user.email == "root@unc.edu"
    assert user.major == "math"

def test_create_user(join_service: JoinService) -> None:
    created_user = join_service.create_user(user)
    assert created_user.email == user.email

def test_create_user_existing_email(join_service: JoinService) -> None:
    with pytest.raises(UserRegistrationException):
        join_service.create_user(updated_root)

def test_update_user(join_service: JoinService) -> None:
    updated_user = join_service.update_user(updated_root)
    assert updated_user.first_name == "updated"
    assert updated_user.last_name == "updated"
    assert updated_user.major == "updated"

def test_update_user_non_existent(join_service: JoinService) -> None:
    with pytest.raises(ResourceNotFoundException):
        join_service.update_user(user)

def test_delete_user(join_service: JoinService) -> None:
    join_service.delete_user(1)
    with pytest.raises(ResourceNotFoundException):
        join_service.get_user(1)

def test_delete_user_non_existent(join_service: JoinService) -> None:
    with pytest.raises(ResourceNotFoundException):
        join_service.delete_user(999)

def test_get_user_by_id_not_found(join_service: JoinService) -> None:
    with pytest.raises(ResourceNotFoundException):
        join_service.get_user(999)

def test_check_email_registered(join_service: JoinService) -> None:
    assert join_service.check_email_registered("root@unc.edu") is True
    assert join_service.check_email_registered("nonexistent@example.com") is False
