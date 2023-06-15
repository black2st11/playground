from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: QuestionCreate, owner_id: int
    ) -> Question:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 10
    ) -> list[Question]:
        return (
            db.query(self.model)
            .filter(Question.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


question = CRUDQuestion(Question)
