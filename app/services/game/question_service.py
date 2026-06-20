from sqlalchemy.orm import Session
from app.models.question import Question
import random


def get_question(db: Session, faculty_id: str = None, difficulty: str = None):
    """
    Returns a single question for gameplay.
    Can be filtered by faculty or difficulty.
    """

    query = db.query(Question)

    if faculty_id:
        query = query.filter(Question.faculty_id == faculty_id)

    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    questions = query.all()

    if not questions:
        return None

    return random.choice(questions)