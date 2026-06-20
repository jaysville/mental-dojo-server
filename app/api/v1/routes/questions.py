from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.game.question_engine import get_next_question
from app.services.game.evaluation_engine import evaluate_answer
from app.models.faculty_progress import FacultyProgress
from app.core.responses import success, error

router = APIRouter()

#should have a general function that accepts the faculty ids and then calls this next with 
#a random faculty from the passed on faculty ids;

@router.post("/next")
def next_question(user_id: str, faculty_id: str, db: Session = Depends(get_db)):
    print(f"Getting next question for user {user_id} in faculty {faculty_id}")

    faculty_progress = db.query(FacultyProgress).filter_by(
        user_id=user_id,
        faculty_id=faculty_id
    ).first()

    question = get_next_question(db, user_id, faculty_id, faculty_progress)

    return success(data=question)


@router.post("/answer")
def submit_answer(
    user_id: str,
    question_id: str,
    answer: str,
    db: Session = Depends(get_db)
):
    return evaluate_answer(db, user_id, question_id, answer)