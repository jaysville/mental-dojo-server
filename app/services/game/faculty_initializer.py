from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.models.faculty_progress import FacultyProgress


def initialize_faculties_for_user(db: Session, user_id: str):
    """
    Ensures every user has progress rows for every faculty.
    This prevents runtime crashes later.
    """

    faculties = db.query(Faculty).all()

    for faculty in faculties:
        existing = db.query(FacultyProgress).filter(
            FacultyProgress.user_id == user_id,
            FacultyProgress.faculty_id == faculty.id
        ).first()

        if not existing:
            db.add(FacultyProgress(
                user_id=user_id,
                faculty_id=faculty.id,
                xp=0,
                level=1,
                attempts=0,
                correct=0,
                streak=0
            ))

    db.commit()