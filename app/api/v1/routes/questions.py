from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.game.question_engine import get_next_question
from app.services.game.evaluation_engine import evaluate_answer
from app.models.faculty_progress import FacultyProgress
from app.core.responses import success
from app.schemas.question import NextQuestionRequest, QuestionResponse
from app.core.auth import get_current_user
from app.schemas.answers import AnswerRequest
import random

router = APIRouter()

#should have a general function that accepts the faculty ids and then calls this next with 
#a random faculty from the passed on faculty ids;

@router.post("/next" , response_model=None)
def next_question(
    request: NextQuestionRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # 👈 inject user
):
    user_id = user.id

    faculty_id = random.choice(request.faculty_ids)

    faculty_progress = db.query(FacultyProgress).filter_by(
        user_id=user_id,
        faculty_id=faculty_id
    ).first()

    question = get_next_question(db, user_id, faculty_id, faculty_progress)

    return success(data=QuestionResponse.model_validate(question).model_dump())

@router.post("/answer")
def submit_answer_route(
    request: AnswerRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return evaluate_answer(
        db=db,
        user_id=user.id,
        question_id=request.question_id,
        user_answer=request.user_answer
    )