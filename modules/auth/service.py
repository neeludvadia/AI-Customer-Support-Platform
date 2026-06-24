from datetime import datetime, timedelta, timezone

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

    def login(self, email: str, password: str) -> tuple[str, str]:
        """Authenticate user and return (access_token, username)."""
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        return create_access_token(user.id), user.username

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)
