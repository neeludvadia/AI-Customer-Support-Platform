from pydantic import BaseModel, EmailStr
from datetime import datetime


# ── Request DTOs ──────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# ── Response DTOs ─────────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Internal ──────────────────────────────────────────────────────────────────

class TokenData(BaseModel):
    user_id: int | None = None
