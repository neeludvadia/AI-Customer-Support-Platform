from fastapi import APIRouter, Depends, HTTPException, Response, status, Request, Cookie
from sqlalchemy.orm import Session

from database.database import get_db
from config.settings import settings
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
def login(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    
    try:
        access_token, refresh_token, username = AuthService(db).login(
            email=payload.email, 
            password=payload.password,
            device_name=user_agent, # Using user_agent as a fallback device name for now
            ip_address=ip_address,
            user_agent=user_agent
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,        # set True in production (HTTPS)
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="username",
        value=username,
        httponly=False,      # readable by JS (not sensitive)
        samesite="lax",
        secure=False,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, response: Response, db: Session = Depends(get_db), refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    
    try:
        new_access_token, new_refresh_token = AuthService(db).refresh_session(
            refresh_token=refresh_token,
            device_name=user_agent,
            ip_address=ip_address,
            user_agent=user_agent
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
    )
    
    return TokenResponse(access_token=new_access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, db: Session = Depends(get_db), refresh_token: str | None = Cookie(default=None)):
    if refresh_token:
        AuthService(db).logout(refresh_token)
        
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    response.delete_cookie(key="username")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
