from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database.database import get_db
from modules.auth.dto import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from modules.auth.service import AuthService
from modules.auth.dependencies import get_current_user
from modules.auth.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService(db).register(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    try:
        token, username = AuthService(db).login(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,        # set True in production (HTTPS)
        max_age=30 * 60,
    )
    response.set_cookie(
        key="username",
        value=username,
        httponly=False,      # readable by JS (not sensitive)
        samesite="lax",
        secure=False,
        max_age=30 * 60,
    )
    return TokenResponse(access_token=token)



@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="username")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
