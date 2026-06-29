from datetime import datetime, timedelta, timezone
import secrets
import hashlib

from jose import jwt
import bcrypt
from sqlalchemy.orm import Session

from config.settings import settings
from modules.auth.models import User
from modules.auth.repository import AuthRepository
from modules.auth.dto import RegisterRequest, TokenData


# ── Password helpers ──────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False


# ── JWT helpers ───────────────────────────────────────────────────────────────

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = payload.get("sub")
    if user_id is None:
        raise ValueError("Invalid token payload")
    return TokenData(user_id=int(user_id))


# ── Refresh Token helpers ─────────────────────────────────────────────────────

def generate_refresh_token() -> str:
    return secrets.token_hex(32)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


# ── Auth service ──────────────────────────────────────────────────────────────

class AuthService:
    def __init__(self, db: Session):
        self.repo = AuthRepository(db)

    def register(self, data: RegisterRequest) -> User:
        if self.repo.get_by_email_or_username(data.email, data.username):
            raise ValueError("Email or username already registered")
        return self.repo.create(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )

    def login(self, email: str, password: str, device_name: str | None = None, ip_address: str | None = None, user_agent: str | None = None) -> tuple[str, str, str]:
        """Authenticate user and return (access_token, refresh_token, username)."""
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        
        access_token = create_access_token(user.id)
        
        refresh_token_plain = generate_refresh_token()
        refresh_token_hashed = hash_token(refresh_token_plain)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        self.repo.save_refresh_token(
            user_id=user.id,
            token_hash=refresh_token_hashed,
            expires_at=expires_at,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent
        )

        return access_token, refresh_token_plain, user.username

    def refresh_session(self, refresh_token: str, device_name: str | None = None, ip_address: str | None = None, user_agent: str | None = None) -> tuple[str, str]:
        """Rotate refresh token and return (new_access_token, new_refresh_token)."""
        token_hash = hash_token(refresh_token)
        db_token = self.repo.find_refresh_token_by_hash(token_hash)
        
        if not db_token:
            raise ValueError("Invalid refresh token")
        
        if db_token.revoked_at:
            raise ValueError("Refresh token has been revoked")
            
        if db_token.expires_at < datetime.now(timezone.utc):
            raise ValueError("Refresh token expired")
            
        # Revoke the old token
        self.repo.revoke_refresh_token(token_hash)
        
        # Generate new tokens
        access_token = create_access_token(db_token.user_id)
        
        new_refresh_plain = generate_refresh_token()
        new_refresh_hashed = hash_token(new_refresh_plain)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        self.repo.save_refresh_token(
            user_id=db_token.user_id,
            token_hash=new_refresh_hashed,
            expires_at=expires_at,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return access_token, new_refresh_plain

    def logout(self, refresh_token: str) -> None:
        token_hash = hash_token(refresh_token)
        self.repo.revoke_refresh_token(token_hash)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)
