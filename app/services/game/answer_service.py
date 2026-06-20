from sqlalchemy.orm import Session
from app.services.game.evaluation_engine import evaluate_answer


def submit_answer(db: Session, user_id: str, question_id: str, answer: str):
    """
    Handles full answer lifecycle:
    - evaluate
    - update XP / streak / levels
    - return result
    """

    return evaluate_answer(
        db=db,
        user_id=user_id,
        question_id=question_id,
        user_answer=answer
    )