"""
The Productivity Service allows the API to manipulate user data in the database.
"""

from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import db_session
from backend.entities.user_entity import UserEntity

from backend.models.user_data import User
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from ..models.user_data import UserData

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class JoinService:
    """Backend service that enables direct modification of user data."""

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initializes the `JoinService` session"""
        self._session = session

    def get_users(self) -> list[UserData]:
        """
        Retrieves all users.

        Returns:
            list[UserData]: All user data for the currently logged in user.
        """
        query_result = self._session.query(UserEntity).all()
        return [user_entity.to_model() for user_entity in query_result]

    def get_user(self, user_id: int) -> UserData:
        """Gets one user  by an ID.

        Args:
            user_id: user  to retrieve.
        Returns:
            UserData: User with the matching ID.
        Raises:
            UserPermissionException: user attempting to retrieve a user that
                they did not create.
            ResourceNotFoundException: user does not exist.
        """
        user_entity = self.get_user_by_id(user_id)
        return user_entity.to_model()          
    
        # TODO: Ensure that the user attempting to retrieve the user is the same as the user
        # who created the user. Raise an exception otherwise.

    def create_user(self, user: UserData) -> UserData:
        """Stores a user in the database.

        Args:
            user: User to store.
        Returns:
            UserData: Created user.
        """
        # Set user id to none if an id was passed in
        if user.id is not None:
            user.id = None

        newUser = UserEntity.from_model(user)
        self._session.add(newUser)
        self._session.commit()
        return newUser.to_model()

    def update_user(self, user: UserData) -> UserData:
        """Modifies one user in the database.

        Args:
            user: Data for a user with modified values.
        Returns:
            UserData: Updated user.
        Raises:
            ResourceNotFoundException: User does not exist.
        """
        user_entity = self.get_user_by_id(user.id)
        user_entity.first_name = user.first_name
        user_entity.last_name = user.last_name
        user_entity.email = user.email
        user_entity.major = user.major
        self._session.commit()
        return user_entity.to_model()

        # TODO: Ensure that the user attempting to update the user is the same as the user
        # who created the user. Raise an exception otherwise.

    

    def delete_user(self, user_id: int) -> None:
        """Deletes one user from the database.

        Args:
            user_id: ID of the user to delete.
        Raises:
            UserPermissionException: Attempting to delete a user that
                they did not create.
            ResourceNotFoundException: User does not exist.
        """
        # TODO: Query the table for the user with the matching id
        query = self.get_user_by_id(user_id)
        self._session.delete(query)
        self._session.commit()    
        
        # TODO: Ensure that the user attempting to delete the user is the same as the user
        # who created the user. Raise an exception otherwise.

    def get_user_by_id(self, user_id: int) -> UserEntity:
        """Gets one user by an ID.

        Args:
            user_id: ID of the user to get
        Returns:
            User: User with the matching ID.
        Raises:
            ResourceNotFoundException: User does not exist.
        """
        query = self._session.get(UserEntity, user_id)
        if query is None:
            raise ResourceNotFoundException("User does not exist.")
        return query 