"""
Configuration settings for InfraFlow AI Platform
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """

    # Application
    APP_NAME: str = "InfraFlow AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://infraflow-ai.vercel.app"
    ]

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/infraflow_ai"
    )
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # AI Services
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # Document Processing
    AZURE_FORM_RECOGNIZER_ENDPOINT: str = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT", "")
    AZURE_FORM_RECOGNIZER_KEY: str = os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")

    # Vector Database
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    WEAVIATE_URL: str = os.getenv("WEAVIATE_URL", "")
    WEAVIATE_API_KEY: str = os.getenv("WEAVIATE_API_KEY", "")

    # File Storage
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "infraflow-documents")

    # Cloudflare R2 (alternative to S3)
    CLOUDFLARE_ACCOUNT_ID: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    CLOUDFLARE_ACCESS_KEY_ID: str = os.getenv("CLOUDFLARE_ACCESS_KEY_ID", "")
    CLOUDFLARE_SECRET_ACCESS_KEY: str = os.getenv("CLOUDFLARE_SECRET_ACCESS_KEY", "")
    R2_BUCKET_NAME: str = os.getenv("R2_BUCKET_NAME", "infraflow-documents")

    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Monitoring
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    POSTHOG_API_KEY: str = os.getenv("POSTHOG_API_KEY", "")

    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # File Upload
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100 MB
    ALLOWED_DOCUMENT_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
