import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.resolve()
load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
SECRET_KEY = os.environ.get("SECRET_KEY")


class Settings(BaseSettings):
    API_NAME: str = "Track"
    DEFAULT_HOST: str = "0.0.0.0"
    DEFAULT_PORT: int = 8000
    description: str = "Track"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")

    lifetime_seconds: int = 3000
    base_dir: Path = Path(__file__).parent.resolve()


settings = Settings()
