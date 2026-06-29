from sqlalchemy.orm import Session
from app.models.question import Question, AnsweredQuestion

from app.services.game.evaluation_engine import evaluate_answer


def submit_answer(db: Session, user_id: str, question_id: str, answer: str):
    """
    Handles full answer lifecycle:
    - evaluate correctness
    - save answer
    - update XP / streak / levels
    - return result
    """

    # Get question
    question = db.query(Question).filter_by(id=question_id).first()

    if not question:
        raise ValueError("Question not found")

    #  Check correctness
    is_correct = question.answer== answer

    #  Save answer (tracking)
    record = AnsweredQuestion(
        user_id=user_id,
        question_id=question.id,
        faculty_id=question.faculty_id,
        is_correct=is_correct
    )

    db.add(record)
    db.commit()

    #  Evaluate (XP, streak, etc.)
    result = evaluate_answer(
        db=db,
        user_id=user_id,
        question_id=question_id,
        user_answer=answer
    )

    return {
        "correct": is_correct,
        "meta": result
    }