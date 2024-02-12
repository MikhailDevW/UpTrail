from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
TEMPLATE_DIR = Path(__file__).parent.parent.parent.resolve()

router = APIRouter(prefix='/tracks', tags=['Tracks'])
templates = Jinja2Templates(
    directory=(TEMPLATE_DIR / 'frontend' / 'templates')
)


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/")
async def submit(request: Request):
    """Тестовая форма, для проверки и обучения."""

    form_data = await request.form()
    name = form_data["name"]
    email = form_data["email"]
    file = form_data["file"]

    return {"name": name, "email": email, "filename": file.filename}


@router.get("/get_tracks")
async def get_tracks(lat=55.4, long=43.4):
    # tracks = get_tracks_from_db(lat, long)
    return {
        "myResponse": "hello",
        "lat": lat,
        "long": long,
    }


@router.get("/get_file")
async def get_data():
    return FileResponse("шаурма.jpg")
