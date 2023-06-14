from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, validator


# Shared properties question model
class QuestionBase(BaseModel):
    title: str
    description: Optional[str] = None
    count: int

    @validator("count")
    def count_must_greater_than_or_equal_to_two(cls, v):
        if v < 2:
            raise ValueError("count must greater than or equal to two")
        return v


# Properties to receive on question creation
class QuestionCreate(QuestionBase):
    pass


# Properties to receive on question update
class QuestionUpdate(QuestionBase):
    pass


# Properties shared by models stored in DB
class QuestionInDBBase(QuestionBase):
    id: int
    owner_id: int | None
    created: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Question(QuestionInDBBase):
    pass


# Properties properties stored in DB
class QuestionInDB(QuestionInDBBase):
    pass
