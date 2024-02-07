from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from main import BASE_DIR

TEMPLATE_DIR = BASE_DIR.parent.resolve()

tracks_api = FastAPI()
templates = Jinja2Templates(
    directory=(TEMPLATE_DIR / 'frontend' / 'templates')
)


@tracks_api.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@tracks_api.post("/submit")
async def submit(request: Request,):
    """Тестовая форма, для проверки и обучения."""
    
    form_data = await request.form()
    name = form_data["name"]
    email = form_data["email"]
    file = form_data["file"]

    return {"name": name, "email": email, "filename": file.filename}


@tracks_api.get("/get_file")
async def get_data():
    return FileResponse("шаурма.jpg")
