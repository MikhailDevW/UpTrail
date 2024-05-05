from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.users.schemas import UserCreate, UserRead

from .auth import auth_backend
from .manager import get_user_manager
from .models import CustomUser

fastapi_users = FastAPIUsers[CustomUser, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(prefix='', tags=['auth'])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
