import token

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.responses import success, error
from app.models import user
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, SuccessTokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.services.game.faculty_initializer import initialize_faculties_for_user

router = APIRouter()

# -------------------------
# SIGNUP
# -------------------------
@router.post("/signup", summary="Create a new user account")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    email = data.email.strip().lower()

    # Check if user already exists by email
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise AppError(status_code=400, message="User already exists", code="USER_ALREADY_EXISTS")

    # Check if username is taken
    existing_username = db.query(User).filter(User.username == data.username).first()
    if existing_username:
        raise AppError(status_code=400, message="Username already taken", code="USERNAME_TAKEN")

    hashed_pw = hash_password(data.password)

    new_user = User(
        username=data.username,
        email=email,
        password=hashed_pw,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    initialize_faculties_for_user(db, new_user.id)
    token = create_access_token({"sub": new_user.email})

    return success({
    "access_token": token,
    "token_type": "bearer",
    "user": {
        "id": str(new_user.id),
        "email": new_user.email,
        "username": new_user.username,
        "xp": new_user.progress.xp if new_user.progress else 0,
        "streak": new_user.progress.streak if new_user.progress else 0,
        "level": new_user.progress.level if new_user.progress else 1
    }
})


# -------------------------
# LOGIN
# -------------------------
@router.post("/login", summary="Authenticate user via email")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    email = data.email.strip().lower()
    
    # Query user from database
    user = db.query(User).filter(User.email == email).first()
 
    if not user:
        raise AppError(
            status_code=404,
            message="User not found",
            code="USER_NOT_FOUND",
        )

    if not verify_password(data.password, user.password):
        raise AppError(
            status_code=401,
            message="Email or password is incorrect!",
            code="INVALID_CREDENTIALS"
        )

    token = create_access_token({"sub": user.email})

    return success({
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "progress": {
                "xp": user.progress.xp if user.progress else 0,
                "streak": user.progress.streak if user.progress else 0,
                "level": user.progress.level if user.progress else 1,
            }
        }
    })