import gc
import uvicorn

from fastapi import FastAPI
from log_conf import LOGGING_CONFIG

from tracks.router import router as router_tracks
from users.router import router as router_users

log_config = LOGGING_CONFIG

gc.disable()
app = FastAPI()

app.include_router(router_tracks)
app.include_router(router_users)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="localhost",
        port=8888,
        reload=True,
        log_config=log_config,
        use_colors=True,
    )
