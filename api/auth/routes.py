from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    role: str = "student"


class LoginResponse(BaseModel):
    token: str
    role: str


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    if not payload.username.strip():
        raise HTTPException(status_code=400, detail="username is required")
    role = payload.role if payload.role in {"student", "teacher", "researcher"} else "student"
    return LoginResponse(token=f"demo-{payload.username}-{role}", role=role)
