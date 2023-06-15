import pytest
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.tests.session import test_db_session
from app import crud
from app.tests.utils.utils import random_email, random_lower_string
from app.core.security import verify_password


@pytest.fixture(scope="module")
def created_user(db_session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(
        email=random_email(), password=random_lower_string(), name="TEST USER"
    )
    user = crud.user.create(db_session, obj_in=user_in)
    return {"user": user, "email": email, "password": password}


class TestUser:
    def test_create_user(self, test_db_session: Session):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(
            email=random_email(), password=random_lower_string(), name="TEST USER"
        )
        user = crud.user.create(test_db_session, obj_in=user_in)
        assert user.email == email
        assert verify_password(password, user.hashed_password)

    def test_authenticate_user(self, test_db_session: Session):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(
            email=random_email(), password=random_lower_string(), name="TEST USER"
        )
        user = crud.user.create(test_db_session, obj_in=user_in)
        authenticated_user = crud.user.authenticate(
            test_db_session, email=email, password=password
        )

        assert authenticated_user
        assert user == authenticated_user
        assert user.email == authenticated_user.email
