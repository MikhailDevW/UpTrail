from fastapi import APIRouter, UploadFile, File, status
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .tracks_manager import TrackManager

TEMPLATE_DIR = Path(__file__).parent.parent.parent.resolve()

router = APIRouter(prefix='/tracks', tags=['Tracks'])
templates = Jinja2Templates(
    directory=(TEMPLATE_DIR / 'frontend' / 'templates')
)


@router.get("/get_tracks")
async def get_tracks(lt_lat=55.4, lt_long=43.4, rb_lat=54, rb_long=42):
    """
    Функция для получение всех треков,
    которые расположены в заданном квадрате.
    """
    # tracks = get_tracks_from_db()
    return {
        "myResponse": "hello"
    }


@router.post("/post_track", status_code=status.HTTP_201_CREATED)
async def post_track(
    track_file: UploadFile = File()
):
    """
    Публикация нового трека.
    Пользователь загружает один файл своего пройденого трека.
    """
    parse_track = TrackManager.get_track(track_file)
    # add_track_2db(
    #     title=info_data.title,
    #     description=info_data.description,
    #     is_public=info_data.is_public,
    #     *parse_track.get_info()
    # )
    return {
        "latitue": parse_track.get_general_info()[0],
        "longitute": parse_track.get_general_info()[1],
        "distance": parse_track.get_general_info()[2],
    }
