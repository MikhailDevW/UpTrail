import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


class Settings(BaseSettings):

    @property
    def database_url_async_psycopg(self):
        return (
            f"postgresql+asyncpg://{DB_USER}:"
            f"{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )


settings = Settings()
