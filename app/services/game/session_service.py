from sqlalchemy.orm import Session
from datetime import datetime
from app.models.game_session import GameSession


def start_session(db: Session, user_id: str):
    session = GameSession(
        user_id=user_id,
        status="active",
        total_xp=0,
        correct_answers=0,
        total_questions=0
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_active_session(db: Session, user_id: str):
    return db.query(GameSession).filter(
        GameSession.user_id == user_id,
        GameSession.status == "active"
    ).first()


def end_session(db: Session, session_id: str):
    session = db.query(GameSession).filter(
        GameSession.id == session_id
    ).first()

    if not session:
        return None

    session.status = "ended"
    session.ended_at = datetime.utcnow()

    db.commit()

    return session