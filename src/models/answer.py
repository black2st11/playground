from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.base_class import Base


class Answer(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created = Column(DateTime(), server_default=func.now())
    question_id = Column(Integer, ForeignKey("question.id"))
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    question = relationship("Question", back_populates="answers")
    owner = relationship("User", back_populates="answers")
