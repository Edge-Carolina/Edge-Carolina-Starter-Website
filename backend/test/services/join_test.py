import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from ...entities.user_entity import UserEntity
from ...models.user_data import UserData
from ...services.join import JoinService
from ...services.exceptions import ResourceNotFoundException

@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@patch.object(UserEntity, "from_model", return_value=Mock(spec=UserEntity))
@patch.object(UserEntity, "to_model", return_value=Mock(spec=UserData))
def setup_user_entity_mocks(from_model_mock: Mock, to_model_mock: Mock):
    pass


# Run the setup function to apply the patches
setup_user_entity_mocks()


def test_create_user(mock_session: Mock):
    join_service = JoinService(session=mock_session)

    new_user_data = UserData(
        id=None,
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        major="Physics",
    )
    new_user_entity = UserEntity.from_model(new_user_data)

    with patch.object(UserEntity, "from_model", return_value=new_user_entity):
        with patch.object(new_user_entity, "to_model", return_value=new_user_data):
            result = join_service.create_user(new_user_data)

            assert result == new_user_data
            mock_session.add.assert_called_once_with(new_user_entity)
            mock_session.commit.assert_called_once()


def test_get_user(mock_session: Mock):
    join_service = JoinService(session=mock_session)

    user_id = 1
    user_entity = UserEntity(
        id=user_id,
        first_name="Bob",
        last_name="Jones",
        email="bob@example.com",
        major="Chemistry",
    )
    user_data = UserData(
        id=user_id,
        first_name="Bob",
        last_name="Jones",
        email="bob@example.com",
        major="Chemistry",
    )

    with patch.object(join_service, "get_user_by_id", return_value=user_entity):
        with patch.object(user_entity, "to_model", return_value=user_data):
            result = join_service.get_user(user_id)

            assert result == user_data


def test_update_user(mock_session: Mock):
    join_service = JoinService(session=mock_session)

    user_id = 2
    updated_user_data = UserData(
        id=user_id,
        first_name="Charlie",
        last_name="Brown",
        email="charlie@example.com",
        major="Mathematics",
    )
    user_entity = UserEntity(
        id=user_id,
        first_name="Charles",
        last_name="Brown",
        email="charlie@example.com",
        major="Math",
    )

    with patch.object(join_service, "get_user_by_id", return_value=user_entity):
        result = join_service.update_user(updated_user_data)

        assert result.first_name == updated_user_data.first_name
        assert result.last_name == updated_user_data.last_name
        assert result.major == updated_user_data.major
        mock_session.commit.assert_called_once()

def test_delete_user(mock_session: Mock):
    join_service = JoinService(session=mock_session)

    user_id = 3
    user_entity = UserEntity(id=user_id, first_name="David", last_name="Green", email="david@example.com", major="Biology")

    with patch.object(join_service, 'get_user_by_id', return_value=user_entity):
        join_service.delete_user(user_id)

        mock_session.delete.assert_called_once_with(user_entity)
        mock_session.commit.assert_called_once()
