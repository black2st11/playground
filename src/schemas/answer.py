from datetime import datetime
from pydantic import BaseModel


# Shared properties question model
class AnswerBase(BaseModel):
    content: str
    name: str


# Properties to receive on question creation
class AnswerCreate(AnswerBase):
    pass


# Properties to receive on question update
class AnswerUpdate(AnswerBase):
    pass


# Properties shared by models stored in DB
class AnswerInDBBase(AnswerBase):
    id: int
    question_id: int
    owner_id: int | None
    created: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Answer(AnswerInDBBase):
    pass


# Properties properties stored in DB
class AnswerInDB(AnswerInDBBase):
    pass
