# app/config.py
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./moderation.db", env="DATABASE_URL")
    OPENAI_API_KEY: str = Field("", env="OPENAI_API_KEY")
    SLACK_WEBHOOK_URL: str = Field("", env="SLACK_WEBHOOK_URL")
    ADMIN_EMAIL: str = Field("", env="ADMIN_EMAIL")
    EMAIL_FROM: str = Field("no-reply@example.com", env="EMAIL_FROM")
    SMTP_HOST: str = Field("", env="SMTP_HOST")
    SMTP_PORT: int = Field(587, env="SMTP_PORT")
    SMTP_USER: str = Field("", env="SMTP_USER")
    SMTP_PASS: str = Field("", env="SMTP_PASS")
    DEV_MODE: bool = Field(True, env="DEV_MODE")

    class Config:
        env_file = ".env"


settings = Settings()
