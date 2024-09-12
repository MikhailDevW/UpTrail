from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # System parametrs
    API_NAME: str
    DESCRIPTION: str
    DEFAULT_HOST: str
    DEFAULT_PORT: int
    SECRET_KEY: str
    BASE_DIR: Path = Path(__file__).parent.resolve()
    DEBUG: bool
    # Cookie parametrs
    COOKIE_NAME: str = "auth_token"
    COOKIE_MAX_AGE: int = 3600
    COOKIE_HTTPONLY: bool = False
    COOKIE_SECURE: bool = False
    COOKIE_SAMSITE: str | None = None
    # DB parametrs
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
