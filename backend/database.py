from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD


class Base(DeclarativeBase):
    pass


def database_url_async():
    return (
        f"postgresql+asyncpg:"
        f"//{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


async_engine = create_async_engine(
    url=database_url_async(),
    echo=True,
    pool_size=5,
)


track_session = async_sessionmaker(bind=async_engine)


async def get_db_version():
    async with async_engine.connect() as db_connection:
        await db_connection.execute(text("SELECT VERSION()"))
