from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

from app.core.database import Base


class FacultyProgress(Base):
    __tablename__ = "faculty_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculties.id"), index=True)

    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

    correct = Column(Integer, default=0)
    attempts = Column(Integer, default=0)

    streak = Column(Integer, default=0)

    # 🧠 ADAPTIVE SYSTEM FIELDS
    recent_correct = Column(Integer, default=0)
    recent_attempts = Column(Integer, default=0)
    recent_accuracy = Column(Integer, default=0)

    last_active = Column(DateTime, default=lambda: datetime.now(timezone.utc))