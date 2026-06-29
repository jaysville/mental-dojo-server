from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ---- PASSWORD ----

def hash_password(password: str):
    """Hash password using argon2 (no 72-byte limit)"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str):
    """Verify password using argon2"""
    return pwd_context.verify(plain, hashed)


# ---- JWT ----

def create_access_token(user):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "user_id": str(user.id),  
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

