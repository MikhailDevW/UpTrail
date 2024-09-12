import logging

from fastapi import APIRouter, File, UploadFile, status

from .tracks_manager import TrackManager

router = APIRouter(prefix='/tracks', tags=['Tracks'])
logger = logging.getLogger("uvicorn.develop")


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
    parsed_track = TrackManager.get_track(track_file)
    return {
        "latitue": parsed_track.get_general_info()[0],
        "longitute": parsed_track.get_general_info()[1],
        "distance": parsed_track.get_general_info()[2],
    }
