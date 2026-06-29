from sqlalchemy.orm import Session
from modules.auth.models import User, RefreshToken
from datetime import datetime, timezone


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_email_or_username(self, email: str, username: str) -> User | None:
        return self.db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

    def create(self, username: str, email: str, hashed_password: str) -> User:
        user = User(username=username, email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save_refresh_token(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
        device_name: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def find_refresh_token_by_hash(self, token_hash: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()

    def revoke_refresh_token(self, token_hash: str) -> None:
        token = self.find_refresh_token_by_hash(token_hash)
        if token and not token.revoked_at:
            token.revoked_at = datetime.now(timezone.utc)
            self.db.commit()

    def delete_expired_refresh_tokens(self) -> None:
        now = datetime.now(timezone.utc)
        self.db.query(RefreshToken).filter(RefreshToken.expires_at < now).delete()
        self.db.commit()
