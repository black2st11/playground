from sqlalchemy.orm import Session

from app import crud
from app.models.answer import Answer
from app.tests.conftest import db_session
from .test_question import create_question_with_owner
from .test_user import create_user

obj_in = {
    "content": "My favorite singer is Michael Jackson",
    "name": "Answer User1",
}


class TestAnswer:
    def test_create_answer(self, db_session: Session):
        created_question = create_question_with_owner(db_session)
        answer = crud.answer.create_with_question(
            db=db_session, obj_in=obj_in, question_id=created_question["id"]
        )
        assert answer
        assert answer.question_id == created_question["id"]
        assert answer.content == obj_in["content"]
        assert answer.name == obj_in["name"]
        assert answer.created

    def test_create_answer_with_owner(self, db_session: Session):
        created_question = create_question_with_owner(db_session)
        answer = crud.answer.create_with_question_and_owner(
            db=db_session,
            obj_in=obj_in,
            question_id=created_question["id"],
            owner_id=created_question["owner"]["id"],
        )

        assert answer
        assert answer.question_id == created_question["id"]
        assert answer.content == obj_in["content"]
        assert answer.name == obj_in["name"]
        assert answer.owner_id == created_question["owner"]["id"]

    def test_get_question_by_owner_id(self, db_session: Session):
        created_question_one = create_question_with_owner(db_session)
        created_question_two = create_question_with_owner(db_session)

        owner_id = created_question_one["owner"]["id"]

        # user 1
        crud.answer.create_with_question_and_owner(
            db=db_session,
            obj_in=obj_in,
            question_id=created_question_one["id"],
            owner_id=owner_id,
        )
        crud.answer.create_with_question_and_owner(
            db=db_session,
            obj_in=obj_in,
            question_id=created_question_two["id"],
            owner_id=owner_id,
        )

        # user2
        crud.answer.create_with_question_and_owner(
            db=db_session,
            obj_in=obj_in,
            question_id=created_question_one["id"],
            owner_id=created_question_two["owner"]["id"],
        )

        answers = crud.answer.get_multi_by_owner(db=db_session, owner_id=owner_id)

        assert answers
        assert 2 == len(answers)
        assert 2 == len(list(filter(lambda a: a.owner_id == owner_id, answers)))

    def test_get_question_by_question_id(self, db_session: Session):
        created_question_one = create_question_with_owner(db_session)
        created_question_two = create_question_with_owner(db_session)
        created_user = create_user(db_session)

        crud.answer.create_with_question_and_owner(
            db=db_session,
            obj_in=obj_in,
            question_id=created_question_one["id"],
            owner_id=created_question_one["owner"]["id"],
        )

        crud.answer.create_with_question_and_owner(
            db=db_session,
            obj_in=obj_in,
            question_id=created_question_one["id"],
            owner_id=created_user["id"],
        )

        crud.answer.create_with_question_and_owner(
            db=db_session,
            obj_in=obj_in,
            question_id=created_question_two["id"],
            owner_id=created_user["id"],
        )

        answers = crud.answer.get_multi_by_question(
            db=db_session, question_id=created_question_one["id"]
        )

        assert answers
        assert 2 == len(answers)
        assert [created_question_one["owner"]["id"], created_user["id"]] == [
            answer.owner_id for answer in answers
        ]
