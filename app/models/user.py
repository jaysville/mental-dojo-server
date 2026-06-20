from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(30), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    # relationships
    progress = relationship("UserProgress", backref="user", uselist=False)

    faculty_progress = relationship(
        "FacultyProgress",
        backref="user",
        cascade="all, delete-orphan"
    )