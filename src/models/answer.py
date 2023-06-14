from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.base_class import Base


class Answer(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    name = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", back_populates="answers")
