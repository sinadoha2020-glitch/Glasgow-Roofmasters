"""Application configuration and settings."""
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = "Glasgow Roofmasters"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"

    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/glasgow_roofmasters.db"

    # Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "Glasgow Roofmasters"
    SMTP_FROM_EMAIL: str = "post@glasgowroofmasters.co.uk"

    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD_HASH: str = ""

    # reCAPTCHA
    RECAPTCHA_SITE_KEY: str = ""
    RECAPTCHA_SECRET_KEY: str = ""

    # Google Maps
    GOOGLE_MAPS_API_KEY: str = ""

    # Business Info (editable CMS fields)
    BUSINESS_PHONE: str = "0141 266 0600"
    BUSINESS_EMAIL: str = "post@glasgowroofmasters.co.uk"
    BUSINESS_ADDRESS: str = "236 Sauchiehall St, Glasgow G2 3HQ"
    BUSINESS_HOURS: str = "Monday–Saturday 9am–6pm, closed Sunday"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
