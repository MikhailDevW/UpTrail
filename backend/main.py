from pathlib import Path

import uvicorn

BASE_DIR = Path(__file__).parent.resolve()

if __name__ == "__main__":
    uvicorn.run(
        app="tracks.api:tracks_api",
        host="localhost",
        port=8888,
        reload=True,
    )
