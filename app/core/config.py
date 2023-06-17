import secrets
from typing import Any

from pydantic import BaseSettings, EmailStr, AnyHttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKENDS_CORS_ORIGINS: list[AnyHttpUrl | str] = []

    @validator("BACKENDS_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URL: PostgresDsn | None = None
    SQLALCHEMY_TEST_DATABASE_URL: PostgresDsn | None = None

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
