from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    UPLOADS_DIR: str = "uploads"
    GEMINI_API_KEY: str = ""
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "kb_documents"
    EMBEDDING_MODEL: str = "gemini-embedding-001"

    class Config:
        env_file = ".env"


settings = Settings()
