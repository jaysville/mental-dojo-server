from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.routes import auth, questions
from app.core.database import engine
from app.core.errors import AppError
from app.core.responses import error

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conn:
            print("✓ Database connection successful")
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise RuntimeError("Database connection failed") from exc
    yield

app = FastAPI(
    title="Mental Dojo API",
    description="The server for Mental Dojo, a web app that helps you learn programming languages by providing interactive coding exercises and real-time feedback.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

api_router = APIRouter(prefix="/api/v1")



@api_router.get("/")
async def root():
    return {"message": "Welcome to the Mental Dojo API!"}


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])

app.include_router(api_router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return error(exc.code, exc.message, exc.fields, status_code=exc.status_code)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return error("HTTP_ERROR", getattr(exc, "detail", "HTTP error"), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error("VALIDATION_ERROR", "Validation failed", exc.errors(), status_code=422)