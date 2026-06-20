from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=15)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=15)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SuccessTokenResponse(BaseModel):
    success: bool
    message: str
    data: TokenResponse