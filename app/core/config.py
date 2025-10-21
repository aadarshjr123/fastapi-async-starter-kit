"""
Application configuration module.

Defines and validates all runtime environment variables using Pydantic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # === Security & Auth ===
    SECRET_KEY: str = "dev_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # === Database ===
    DATABASE_URL: str = "postgresql+asyncpg://myuser:mypassword@db:5432/mydb"

    # === Redis ===
    REDIS_URL: str = "redis://redis:6379"

    # === General ===
    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    PROFILE: int = 0
    POSTGRES_USER: str = "myuser"
    POSTGRES_PASSWORD: str = "mypassword"
    POSTGRES_DB: str = "mydb"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Global instance
settings = Settings()
