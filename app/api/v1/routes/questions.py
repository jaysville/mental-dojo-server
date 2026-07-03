from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.game.question_engine import get_next_question
from app.services.game.evaluation_engine import evaluate_answer
from app.services.game.session_service import get_active_session, start_session
from app.services.game.faculty_initializer import initialize_faculties_for_user
from app.models.faculty_progress import FacultyProgress
from app.core.errors import AppError
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

    # Ensure a game session exists for this user before selecting a question
    session = get_active_session(db, user_id)
    if not session:
        start_session(db, user_id)

    faculty_id = random.choice(request.faculty_ids)

    faculty_progress = db.query(FacultyProgress).filter_by(
        user_id=user_id,
        faculty_id=faculty_id
    ).first()

    if not faculty_progress:
        initialize_faculties_for_user(db, user_id)
        faculty_progress = db.query(FacultyProgress).filter_by(
            user_id=user_id,
            faculty_id=faculty_id
        ).first()

    question = get_next_question(db, user_id, faculty_id, faculty_progress)

    if not question:
        raise AppError(status_code=404, message="No available question found for this faculty", code="QUESTION_NOT_FOUND")

    return success(data=QuestionResponse.model_validate(question).model_dump())

@router.post("/answer")
def submit_answer_route(
    request: AnswerRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    result = evaluate_answer(
        db=db,
        user_id=user.id,
        question_id=request.question_id,
        user_answer=request.user_answer
    )

    return success(data=result)

    return success(data=result)