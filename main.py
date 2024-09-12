import uvicorn
from fastapi import FastAPI

from src.config import settings
from src.log_conf import LOGGING_CONFIG
from src.tracks.router import router as router_tracks
from src.users.router import router as router_users

app = FastAPI()
app.include_router(router_tracks)
app.include_router(router_users)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.DEFAULT_HOST,
        port=settings.DEFAULT_PORT,
        reload=True,
        log_config=LOGGING_CONFIG,
    )
