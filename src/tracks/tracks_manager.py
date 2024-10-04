import logging
import os
from tempfile import SpooledTemporaryFile

import gpxpy
from fastapi import status
from fastapi.exceptions import HTTPException
from lxml import etree

from src.config import settings

from .constants import (
    GPS_TESTFILES_DIR, GPX_XSD_CUSTOM, GPX_XSD_STRICT, GPX_XSD_STRICT_V2
)

logger = logging.getLogger("uvicorn.develop")


class TrackManager:
    """
    Общие методы работы с треками.
    Обработка сырых данных, форматов, валидация первичная и тд.
    Некоторые базовые расчеты (расстояние между двумя точками).
    """

    RADIAN_COEFF: float = 0.01744  # Преобразуем радианы в градусы
    EARTH_RADIUS: int = 6371  # Радиус земли. Усредненный

    GPX_SCHEMA_GPX10: str = (
        settings.BASE_DIR / GPS_TESTFILES_DIR / GPX_XSD_STRICT)
    GPX_SCHEMA_GPX11: str = (
        settings.BASE_DIR / GPS_TESTFILES_DIR / GPX_XSD_STRICT_V2)
    GPX_SCHEMA_UPTRAIL: str = (
        settings.BASE_DIR / GPS_TESTFILES_DIR / GPX_XSD_CUSTOM)

    @classmethod
    def __get_format(cls, track: str) -> str:
        """Получаем формат файла."""
        split_name: list[str] = track.filename.split(".")
        if str(split_name[-1]) != "gpx":
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Incorrect file format."
            )
        return "gpx"

    @classmethod
    def get_track(cls, track_file: SpooledTemporaryFile):
        """Отдаем обьект трека."""
        if not (
            cls.__get_format(track_file) == "gpx"
            and cls.__gpx_validate(track_file)
        ):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Not valid file schema."
            )
        track = gpxpy.parse(track_file.file)
        return track

    @classmethod
    def __gpx_validate(
        cls,
        track_file,
        valid_schema=GPX_SCHEMA_UPTRAIL
    ) -> bool:
        """
        Валидация gpx файла. Но пока не реализовано и не работает.
        Надо смотреть дополнительно попоже.
        """
        # Сохраняем загруженный файл во временный файл
        with open(f"temp_{track_file.filename}", "wb") as temp_file:
            temp_file.write(track_file.file.read())
        # Читаем данные из временного файла и создаем XML дерево
        tree = etree.parse(temp_file.name)
        root = tree.getroot()
        # Определяем схему XSD
        schema = etree.XMLSchema(file=valid_schema)

        # Проверяем соответствие XML данных схеме XSD
        if not schema.validate(root):
            os.remove(settings.BASE_DIR / f"temp_{track_file.filename}")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "XML is not valid."
            )
        os.remove(f"temp_{track_file.filename}")
        track_file.file.seek(0)
        return True
