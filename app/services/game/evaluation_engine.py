from sqlalchemy.orm import Session
from datetime import datetime

from app.core.errors import AppError
from app.models.question import Question, AnsweredQuestion
from app.models.user_progress import UserProgress
from app.models.faculty_progress import FacultyProgress

from app.services.game.faculty_decay import decay_recent_stats
from app.services.game.xp_engine import calculate_xp
from app.services.game.level_engine import calculate_global_level, calculate_faculty_level
from app.services.game.streak_engine import update_streak
from app.services.game.session_service import get_active_session, start_session


def evaluate_answer(
    db: Session,
    user_id: str,
    question_id: str,
    user_answer: str
) -> dict:
    
    session = get_active_session(db, user_id)

    if not session:
        session = start_session(db, user_id)

    # 1. GET QUESTION
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise AppError(status_code=404, message="Question not found", code="QUESTION_NOT_FOUND")

    # 2. GET USER PROGRESS
    user_progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).first()

    if not user_progress:
        user_progress = UserProgress(user_id=user_id, xp=0, streak=0, level=1)
        db.add(user_progress)
        db.commit()

    # 3. GET FACULTY PROGRESS
    faculty_progress = db.query(FacultyProgress).filter(
        FacultyProgress.user_id == user_id,
        FacultyProgress.faculty_id == question.faculty_id
    ).first()

    # AUTO FIX: if missing, create it
    if not faculty_progress:
        from app.services.game.faculty_initializer import initialize_faculties_for_user

        initialize_faculties_for_user(db, user_id)

        faculty_progress = db.query(FacultyProgress).filter(
            FacultyProgress.user_id == user_id,
            FacultyProgress.faculty_id == question.faculty_id
        ).first()

    # 4. CHECK ANSWER
    is_correct = user_answer.strip().lower() == question.answer.strip().lower()

    # 5. SAVE ANSWER RECORD
    answer_record = AnsweredQuestion(
        user_id=user_id,
        question_id=question.id,
        faculty_id=question.faculty_id,
        is_correct=is_correct
    )
    db.add(answer_record)

    # 6. UPDATE STREAK
    faculty_progress.streak = update_streak(
        faculty_progress.last_active,
        faculty_progress.streak
    )

    # 7. CALCULATE XP
    xp_result = calculate_xp(
        difficulty=question.difficulty,
        is_correct=is_correct,
        streak=faculty_progress.streak
    )

    xp_gained = xp_result.xp

    session.total_xp += xp_gained
    session.total_questions += 1

    if is_correct:
        session.correct_answers += 1

    # 7. UPDATE GLOBAL PROGRESS
    user_progress.xp += xp_gained
    user_progress.level = calculate_global_level(user_progress.xp)


    # 8. UPDATE FACULTY PROGRESS
    faculty_progress.xp += xp_gained
    faculty_progress.attempts += 1

    if is_correct:
        faculty_progress.correct += 1
        faculty_progress.recent_correct += 1

    faculty_progress.recent_attempts += 1

    faculty_progress.level = calculate_faculty_level(faculty_progress.xp)
    faculty_progress.last_active = datetime.utcnow()


    # 9. RECALCULATE RECENT ACCURACY (SAFE)
    if faculty_progress.recent_attempts > 0:
        faculty_progress.recent_accuracy = int(
            (faculty_progress.recent_correct / faculty_progress.recent_attempts) * 100
        )
    else:
        faculty_progress.recent_accuracy = 0


    # 10. OPTIONAL DECAY (PREVENT INFINITE MEMORY BLOAT)
    if faculty_progress.recent_attempts % 20 == 0:
        decay_recent_stats(faculty_progress)


    # 11. SAVE

    db.commit()

    return {
        "correct": is_correct,
        "xp_gained": xp_gained,
        "global_level": user_progress.level,
        "faculty_level": faculty_progress.level,
        "streak": faculty_progress.streak,
        "explanation": question.explanation,
    }