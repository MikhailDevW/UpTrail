from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from .auth import auth_backend
from .models import User
from .manager import get_user_manager


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(prefix='/ololo', tags=['ololo'])
current_user = fastapi_users.current_user()


@router.get("/ololo")
async def ololo(user=Depends(current_user)):
    return {
        "tracks": "ok",
    }
