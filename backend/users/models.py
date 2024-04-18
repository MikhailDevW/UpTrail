from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase)
from sqlalchemy import Boolean, String, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, database_url_async


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


engine = create_async_engine(database_url_async())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
