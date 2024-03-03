"""
The Productivity Service allows the API to manipulate pomodoro timer data in the database.
"""

from fastapi import Depends
from pytest import Session
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

    def get_timers(self) -> list[UserData]:
        """
        Retrieves all users.

        Returns:
            list[UserData]: All user data for the currently logged in user.
        """
        # TODO: Query the PomodoroTimer table to retrieve the entries associated with the current user.

        # TODO: Return all the PomodoroTimer entities for the user in the correct format.
        return ...

    def get_timer(self, user_id: int) -> UserData:
        """Gets one timer by an ID.

        Args:
            user_id: Timer to retrieve.
        Returns:
            UserData: User with the matching ID.
        Raises:
            UserPermissionException: user attempting to retrieve a user that
                they did not create.
            ResourceNotFoundException: user does not exist.
        """
        # TODO: Query the PomodoroTimer table to retrieve the timer with the matching id

        # TODO: Add error handling if there is no timer associated with the given id.
        # Check if result is null and raise the custom ResourceNotFoundException

        # TODO: Ensure that the user attempting to retrieve the timer is the same as the user
        # who created the timer. Raise an exception otherwise.

        # TODO: Return the timer if it exists
        return ...

    def create_timer(self, user: UserData) -> UserData:
        """Stores a user in the database.

        Args:
            user: User to store.
        Returns:
            UserData: Created user.
        """
        # Set timer id to none if an id was passed in
        if user.id is not None:
            user.id = None

        # TODO: Create a new timer entity for the table.

        # TODO: Return the new pomodoro timer object.
        return ...

    def update_timer(self, user: UserData) -> UserData:
        """Modifies one user in the database.

        Args:
            user: Data for a user with modified values.
        Returns:
            User: Updated user.
        Raises:
            UserPermissionException: Attempting to update a user that
                they did not create.
            ResourceNotFoundException: User does not exist.
        """
        # TODO: Query the table for the pomodoro with the matching id

        # TODO: Throw the custom ResourceNotFoundException if the user tries to edit a timer
        # that does not exist.

        # TODO: Ensure that the user attempting to update the timer is the same as the user
        # who created the timer. Raise an exception otherwise.

        # TODO: Update each field of the pomodoro timer object to match the fields of the given timer.

        # TODO: Return the updated pomodoro timer object
        return ...

    def delete_timer(self, user_id: int) -> None:
        """Deletes one user from the database.

        Args:
            user_id: ID of the user to delete.
        Raises:
            UserPermissionException: Attempting to delete a user that
                they did not create.
            ResourceNotFoundException: User does not exist.
        """
        # TODO: Query the table for the pomodoro with the matching id

        # TODO: Throw the custom ResourceNotFoundException if the user tries to delete a timer
        # that does not exist.

        # TODO: Ensure that the user attempting to delete the timer is the same as the user
        # who created the timer. Raise an exception otherwise.

        # TODO: Delete the pomodoro entity from the table/session.

        # TODO: Commit the changes to the table/session.