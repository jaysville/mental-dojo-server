from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.game.session_service import start_session, end_session, get_active_session

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/start")
def start_game_session(req: dict, db: Session = Depends(get_db)):
    session = start_session(db, req["user_id"])

    return {
        "session_id": str(session.id),
        "status": session.status
    }


@router.post("/end")
def end_game_session(req: dict, db: Session = Depends(get_db)):
    session = end_session(db, req["session_id"])

    return {
        "session_id": str(session.id),
        "status": session.status,
        "total_xp": session.total_xp,
        "correct": session.correct_answers,
        "questions": session.total_questions
    }


@router.get("/active/{user_id}")
def get_session(user_id: str, db: Session = Depends(get_db)):
    session = get_active_session(db, user_id)

    if not session:
        return {"active": False}

    return {
        "active": True,
        "session_id": str(session.id)
    }