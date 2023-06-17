from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from .test_user import CreatedUser
from app import crud
from app.tests.conftest import db_session
from .test_user import create_user
from app.models.question import Question


class CreatedQuestion(BaseModel):
    id: int
    title: str
    description: str
    owner: CreatedUser


def create_question_with_owner(db_session) -> CreatedQuestion:
    created_user = create_user(db_session)
    obj_in = {
        "title": "Who is your favorite singer?",
        "description": "You must answer this question",
        "count": 2,
    }
    question = crud.question.create_with_owner(
        db=db_session, obj_in=obj_in, owner_id=created_user["id"]
    )

    return {
        "id": question.id,
        "title": question.title,
        "desciption": question.description,
        "owner": created_user,
    }


def create_multiple_question(db_session: Session, count: int = 2) -> CreatedUser:
    created_user = create_user(db_session)
    for i in range(1, count + 1):
        question = Question(
            **jsonable_encoder(
                {
                    "title": f"Question {i}",
                    "description": f"Description {i}",
                    "count": 2,
                }
            ),
            owner_id=created_user["id"],
        )
        db_session.add(question)
    db_session.commit()
    return created_user


class TestQuestion:
    def test_update(self, db_session):
        created_question = create_question_with_owner(db_session)
        question = crud.question.get(db_session, id=created_question["id"])
        obj_in = {
            "title": "What's your favorite fruit?",
            "description": "If you can't answer this question, you should submit x",
            "count": 3,
        }
        updated_question = crud.question.update(
            db=db_session, db_obj=question, obj_in=obj_in
        )
        assert updated_question.title == obj_in["title"]
        assert updated_question.count == obj_in["count"]
        assert updated_question.description == obj_in["description"]

    def test_create_with_owner(self, db_session):
        created_user = create_user(db_session)
        obj_in = {
            "title": "Who is your favorite singer?",
            "description": "You must answer this question",
            "count": 2,
        }
        question = crud.question.create_with_owner(
            db=db_session, obj_in=obj_in, owner_id=created_user["id"]
        )

        assert question.owner_id == created_user["id"]

    def test_get_multi_by_owner(self, db_session):
        created_user = create_multiple_question(db_session, 10)
        questions = crud.question.get_multi_by_owner(
            db_session, owner_id=created_user["id"]
        )
        assert 10 == len(questions)
        assert 10 == len(
            list(filter(lambda q: q.owner.id == created_user["id"], questions))
        )
