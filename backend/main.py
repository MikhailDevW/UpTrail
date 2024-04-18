import gc
import uvicorn

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from log_conf import LOGGING_CONFIG

from tracks.router import router as router_tracks
from users.router import router as router_users
from users.auth import auth_backend
from users.schemas import UserRead, UserCreate
from users.models import User
from users.manager import get_user_manager
from users.router import fastapi_users

log_config = LOGGING_CONFIG

gc.disable()

# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )

app = FastAPI()


app.include_router(router_tracks)
app.include_router(router_users)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Autharization"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Autharization"],
)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="localhost",
        port=8888,
        reload=True,
        log_config=log_config,
        use_colors=True,
    )
