"""Mock data for users.

Three users are setup for testing and development purposes:

1. Rhonda Root (root user with all permissions)
2. Amy Ambassador (staff of XL with elevated permissions)
3. Sally Student (standard user without any special permissions)"""

import pytest
from sqlalchemy.orm import Session
from backend.entities.user_entity import UserEntity

from backend.models.user_data import UserData
from backend.test.services.reset_table_id_seq import reset_table_id_seq

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

root = UserData(
    id=1,
    first_name="root",
    last_name="root",
    email="root@unc.edu",
    major="math"
)

updated_root = UserData(
    id=1,
    first_name="updated",
    last_name="updated",
    email="root@unc.edu",
    major="updated"
)

user = UserData(
    id=2,
    first_name="user",
    last_name="user",
    email="user@unc.edu",
    major="phyics"
)
users = [root]


def insert_fake_data(session: Session):
    global users
    entities = []
    for user in users:
        entity = UserEntity.from_model(user)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)
    session.commit()  # Commit to ensure User IDs in database


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
