from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import db_session
from ..entities.user_entity import UserEntity
from ..models.user_data import UserData
from ..services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
    UserRegistrationException,
)

class JoinService:
    """Backend service that enables direct modification of user data."""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes the `JoinService` session"""
        self._session = session

    def get_users(self) -> list[UserData]:
        """Retrieves all users."""
        query_result = self._session.query(UserEntity).all()
        return [user_entity.to_model() for user_entity in query_result]

    def get_user(self, user_id: int) -> UserData:
        """Gets one user by an ID."""
        user_entity = self._session.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise ResourceNotFoundException("User does not exist.")
        return user_entity.to_model()

    def create_user(self, user: UserData) -> UserData:
        """Stores a user in the database."""
        existing_email = self._session.query(UserEntity).filter(UserEntity.email == user.email).first()
        if existing_email:
            raise UserRegistrationException()

        new_user = UserEntity.from_model(user)
        self._session.add(new_user)
        self._session.commit()
        return new_user.to_model()

    def update_user(self, user: UserData) -> UserData:
        """Modifies one user in the database."""
        user_entity = self._session.query(UserEntity).filter(UserEntity.id == user.id).first()
        if user_entity is None:
            raise ResourceNotFoundException("User does not exist.")

        user_entity.first_name = user.first_name
        user_entity.last_name = user.last_name
        user_entity.email = user.email
        user_entity.major = user.major
        self._session.commit()
        return user_entity.to_model()

    def delete_user(self, user_id: int) -> None:
        """Deletes one user from the database."""
        user_entity = self._session.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise ResourceNotFoundException("User does not exist.")

        self._session.delete(user_entity)
        self._session.commit()

    def check_email_registered(self, email: str) -> bool:
        """Checks if an email is already registered."""
        existing_email = self._session.query(UserEntity).filter(UserEntity.email == email).first()
        return existing_email is not None
