from pydantic import BaseModel
from uuid import UUID

class AnswerRequest(BaseModel):
    question_id: UUID
    user_answer: str