from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.base_class import Base


class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    count = Column(Integer, CheckConstraint("count > 1"), default=2)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    created = Column(DateTime(), server_default=func.now())
    owner = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
