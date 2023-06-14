from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.base_class import Base


class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    count = Column(Integer, default=2)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    owner = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
