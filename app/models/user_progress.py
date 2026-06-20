from sqlalchemy import Column, Integer, DateTime, ForeignKey, UUID, JSON
from app.core.database import Base
from datetime import datetime, timezone
import uuid


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)

    xp = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # 🧠 NEW: per-faculty progression system
    faculty_xp = Column(JSON, default=dict)
    faculty_levels = Column(JSON, default=dict)

    last_active = Column(DateTime, default=lambda: datetime.now(timezone.utc))