from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)

    status = Column(String, default="active")  # active | ended

    total_xp = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)

    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime, nullable=True)