from sqlalchemy import func
from app.models.question import Question, AnsweredQuestion

from app.services.game.difficulty_engine import calculate_next_difficulty


def get_next_question(db, user_id, faculty_id, faculty_progress):

    #Determine difficulty
    difficulty = calculate_next_difficulty(faculty_progress)

    #Subquery of answered questions
    answered_ids = (
        db.query(AnsweredQuestion.question_id)
        .filter_by(user_id=user_id, faculty_id=faculty_id)
    )

    #  Main query 
    question = (
        db.query(Question)
        .filter(
            Question.faculty_id == faculty_id,
            Question.difficulty == difficulty,
            ~Question.id.in_(answered_ids)
        )
        .order_by(func.random())
        .first()
    )

    return question