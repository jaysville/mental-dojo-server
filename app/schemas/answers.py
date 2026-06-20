from pydantic import BaseModel
from uuid import UUID

class AnswerRequest(BaseModel):
    user_id: UUID
    question_id: UUID
    answer: str