import logging
from lxml import etree
import os
from typing import Union
from typing_extensions import Annotated

from fastapi import (
    APIRouter, File, Path as Api_Path, Query, status, UploadFile,
)

from config import BASE_DIR
from database import add_track, get_all_tracks
from .tracks_manager import TrackManager


router = APIRouter(prefix='/tracks', tags=['Tracks'])
logger = logging.getLogger("uvicorn.develop")


@router.get("/get_tracks")
async def get_tracks(
    lt_lat: Annotated[Union[int, float], Query(ge=-90, le=90)] = 55,
    lt_long: Annotated[Union[int, float], Query(ge=-90, le=90)] = 43,
    rb_lat: Annotated[Union[int, float], Query(ge=-90, le=90)] = 54,
    rb_long: Annotated[Union[int, float], Query(ge=-90, le=90)] = 42,
):
    """
    Функция для получение всех треков,
    которые расположены в заданном квадрате.
    """
    logger.debug(msg="enter in func")
    res = await get_all_tracks(lt_lat, lt_long, rb_lat, rb_long)
    return {
        "tracks": res,
    }


@router.post("/post_track", status_code=status.HTTP_201_CREATED)
async def post_track(track_file: UploadFile = File(...)):
    """
    Публикация нового трека.
    Пользователь загружает один файл своего пройденого трека.
    """
    logger.debug(msg="enter in func")
    parsed_track = TrackManager.get_track(track_file)
    await add_track(
        parsed_track.get_general_info()[0],
        parsed_track.get_general_info()[1],
        parsed_track.get_general_info()[2],
    )
    return {
        "latitue": parsed_track.get_general_info()[0],
        "longitute": parsed_track.get_general_info()[1],
        "distance": parsed_track.get_general_info()[2],
    }


@router.patch("/track/{track_id}")
async def patch_track(track_id: Annotated[int, Api_Path(gt=0)]):
    return {track_id: "patched"}


@router.delete("/track/{track_id}")
async def delete_track(track_id: Annotated[int, Api_Path(gt=0)]):
    return {track_id: "deleted"}


@router.post("/validate_xml/")
async def upload_xml(file: UploadFile = File(...)):
    """
    Некий такой сервисный урл на время для проверки трееков.
    Проверяем заранее валидный трек, проходит ли он проверку или нет.
    Ну и можно использовать для настрйоки шаблона валидации.
    """
    # Сохраняем загруженный файл во временный файл
    with open(f"temp_{file.filename}", "wb") as temp_file:
        temp_file.write(await file.read())

    # Читаем данные из временного файла и создаем XML дерево
    tree = etree.parse(temp_file.name)
    root = tree.getroot()

    # Определяем схему XSD
    valid_schema = BASE_DIR / "gps_test_files/uptrail_custom.xsd"
    schema = etree.XMLSchema(file=valid_schema)

    # Проверяем соответствие XML данных схеме XSD
    if not schema.validate(root):
        os.remove(BASE_DIR / f"temp_{file.filename}")
        return {"message": "XML data is not valid."}
    os.remove(BASE_DIR / f"temp_{file.filename}")
    return {"message": "XML data is valid."}
