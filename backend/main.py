import gc

from fastapi import FastAPI
import uvicorn
from tracks.router import router as router_tracks

gc.disable()
app = FastAPI()

app.include_router(router_tracks)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="localhost",
        port=8888,
        reload=True,
    )
