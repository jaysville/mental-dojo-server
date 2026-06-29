from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
from app.core.database import Base
import uuid


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculties.id"), nullable=False)

    difficulty = Column(String(20))
    type = Column(String(20))  # mcq | input

    question = Column(String, nullable=False)

    options = Column(ARRAY(String), nullable=True)
    answer = Column(String, nullable=False)

    explanation = Column(String, nullable=True)

    created_at = Column(DateTime, default=func.now())


class AnsweredQuestion(Base):
    __tablename__ = "answered_questions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    question_id = Column(Integer)
    faculty_id = Column(String)    