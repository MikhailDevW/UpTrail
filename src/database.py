from typing import AsyncGenerator

from sqlalchemy import Integer, text
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings


def database_url_async():
    return (
        f"postgresql+asyncpg:"
        f"//{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:"
        f"{settings.DB_PORT}/{settings.DB_NAME}"
    )


async_engine = create_async_engine(
    url=database_url_async(),
    echo=True if settings.DEBUG else False,
    pool_size=5,
)
async_session = async_sessionmaker(bind=async_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_db_version():
    async with async_engine.connect() as db_connection:
        await db_connection.execute(text("SELECT VERSION()"))


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
