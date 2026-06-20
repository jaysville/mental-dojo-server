from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "supersecretkey"  # move to .env later
ALGORITHM = "HS256"
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

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)