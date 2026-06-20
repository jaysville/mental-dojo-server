from sqlalchemy import func
from app.models.question import Question
from app.services.game.difficulty_engine import calculate_next_difficulty


def get_next_question(db, user_id, faculty_id, faculty_progress):
    difficulty = calculate_next_difficulty(faculty_progress)

    question = (
        db.query(Question)
        .filter(
            Question.faculty_id == faculty_id,
            Question.difficulty == difficulty
        )
        .order_by(func.random())
        .first()
    )

    return question