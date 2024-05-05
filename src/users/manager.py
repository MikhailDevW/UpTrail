from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_async_session

from .models import CustomUser


class UserManager(IntegerIDMixin, BaseUserManager[CustomUser, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(
        self, user: CustomUser, request: Optional[Request] = None
    ):
        pass

    async def on_after_forgot_password(
        self, user: CustomUser, token: str, request: Optional[Request] = None
    ):
        pass

    async def on_after_request_verify(
        self, user: CustomUser, token: str, request: Optional[Request] = None
    ):
        pass


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, CustomUser)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
