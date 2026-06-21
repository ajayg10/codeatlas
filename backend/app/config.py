"""
Application configuration using pydantic-settings.
All settings are loaded from environment variables or .env file.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/opensource_mentor"

    # Cognee Cloud
    COGNEE_API_URL: str = ""
    COGNEE_API_KEY: str = ""

    # GitHub
    GITHUB_TOKEN: str = ""

    # LLM Provider: "openai" or "gemini"
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Auth
    JWT_SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Ingestion limits (reduced for MVP speed)
    MAX_ISSUES: int = 5
    MAX_PRS: int = 5
    MAX_DISCUSSIONS: int = 5

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
