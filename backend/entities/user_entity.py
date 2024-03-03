"""Definition of SQLAlchemy table-backed object mapping entity for Users."""
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self

from  backend.models.user_data import UserData
from .entity_base import EntityBase

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class UserEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `UserData` table"""

    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint('email'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    major: Mapped[str] = mapped_column(String(50))

    # Example relationship (if applicable)
    # posts = relationship("PostEntity", back_populates="user")

    @classmethod
    def from_model(cls, model: UserData) -> Self:
        """
        Create a UserEntity from a UserData model.

        Args:
            model (UserData): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted).
        """
        return cls(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            major=model.major,
        )

    def to_model(self) -> UserData:
        """
        Create a UserData model from a UserEntity.

        Returns:
            User: A UserData model for API usage.
        """
        return UserData(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            major=self.major,
        )