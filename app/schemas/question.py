from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class NextQuestionRequest(BaseModel):
    faculty_ids: List[str]


class QuestionResponse(BaseModel):
    id: UUID
    faculty_id: UUID
    difficulty: str
    type: str
    question: str
    options: Optional[list[str]] = None
    answer: str
    explanation: str
    created_at: datetime

    class Config:
        from_attributes = True    