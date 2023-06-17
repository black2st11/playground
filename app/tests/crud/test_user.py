from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app import crud
from app.tests.utils.utils import random_email, random_lower_string
from app.core.security import verify_password
from app.tests.conftest import db_session
from app.models.user import User
from app.core.security import get_password_hash


class CreatedUser(BaseModel):
    id: int
    email: str
    password: str


def create_user(db_session: Session) -> CreatedUser:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, name="TEST USER")
    user = crud.user.create(db_session, obj_in=user_in)
    return {"id": user.id, "email": email, "password": password}


def create_multiple_user(db_session: Session, count: int = 2) -> None:
    for i in range(1, count + 1):
        obj_in = {
            "email": f"user{i}@playground.com",
            "hashed_password": get_password_hash(random_lower_string()),
            "name": f"User {i}",
        }

        db_session.add(User(**obj_in))
    db_session.commit()


class TestUser:
    def test_create_user(self, db_session: Session):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(email=email, password=password, name="TEST USER")
        user = crud.user.create(db_session, obj_in=user_in)
        assert user.email == email
        assert verify_password(password, user.hashed_password)

    def test_authenticate_user(self, db_session: Session):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(email=email, password=password, name="TEST USER")
        user = crud.user.create(db_session, obj_in=user_in)
        authenticated_user = crud.user.authenticate(
            db_session, email=email, password=password
        )

        assert authenticated_user
        assert user == authenticated_user
        assert user.email == authenticated_user.email

    def test_get_by_email(self, db_session: Session):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(email=email, password=password, name="TEST USER")
        crud.user.create(db_session, obj_in=user_in)
        user = crud.user.get_by_email(db_session, email=email)
        assert user
        assert user.email == email

    def test_user_update(self, db_session):
        created_user = create_user(db_session)
        user = crud.user.get_by_email(db_session, email=created_user["email"])
        obj_in = {"email": random_email()}
        updated_user = crud.user.update(db=db_session, db_obj=user, obj_in=obj_in)
        assert updated_user.email == obj_in["email"]

    def test_user_remove(self, db_session):
        created_user = create_user(db_session)
        assert crud.user.remove(db=db_session, id=created_user["id"])
        assert crud.user.get(db_session, id=created_user["id"]) == None

    def test_user_get(self, db_session):
        created_user = create_user(db_session)
        user = crud.user.get(db_session, created_user["id"])

        assert user
        assert user.id == created_user["id"]

    def test_get_multiple_user(self, db_session):
        create_multiple_user(db_session, 11)
        assert 10 == len(crud.user.get_multi(db=db_session, offset=0, limit=10))
        assert 5 == len(crud.user.get_multi(db=db_session, offset=0, limit=100))
