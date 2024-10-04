import logging
from typing import Union

from fastapi import APIRouter, File
from fastapi import Path as Api_Path
from fastapi import Query, UploadFile, status
from typing_extensions import Annotated

# from src.users.router import current_user
from .crud import get_all_tracks
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


@router.post(
    "/post_track",
    # dependencies=[Depends(current_user)],
    status_code=status.HTTP_201_CREATED,
)
async def post_track(
    track_file: UploadFile = File(...),
):
    """
    Публикация нового трека.
    Пользователь загружает один файл своего пройденого трека.
    """
    logger.debug(msg="enter in func")
    parsed_track = TrackManager.get_track(track_file)
    # await add_track(
    #     parsed_track.get_general_info()[0],
    #     parsed_track.get_general_info()[1],
    #     parsed_track.get_general_info()[2],
    # )
    start_point = parsed_track.tracks[0].segments[0].points[0]
    return {
        "latitude": start_point.latitude,
        "longitude": start_point.latitude,
        "distance": parsed_track.length_2d()
    }


@router.patch("/track/{track_id}")
async def patch_track(track_id: Annotated[int, Api_Path(gt=0)]):
    return {track_id: "patched"}


@router.delete("/track/{track_id}")
async def delete_track(track_id: Annotated[int, Api_Path(gt=0)]):
    return {track_id: "deleted"}
