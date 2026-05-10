from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "NextRole - AI Opportunity Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/student_opportunities",
    )
    DATABASE_ECHO: bool = False

    # JWT & Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Embeddings
    EMBEDDING_DIMENSION: int = 1536
    SEMANTIC_SEARCH_THRESHOLD: float = 0.6
    MAX_SEARCH_RESULTS: int = 50

    # Scraping
    SCRAPER_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost",
    ]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Background jobs
    SCHEDULER_ENABLED: bool = True
    CHECK_EXPIRED_INTERVAL_HOURS: int = 6
    REFRESH_EMBEDDINGS_INTERVAL_HOURS: int = 24
    SCRAPER_RUN_INTERVAL_HOURS: int = 12

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
