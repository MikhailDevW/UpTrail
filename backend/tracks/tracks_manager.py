import os
import logging
from tempfile import SpooledTemporaryFile

import gpxpy
from fastapi import status
from fastapi.exceptions import HTTPException
from haversine import haversine, Unit
from lxml import etree

from config import BASE_DIR

logger = logging.getLogger("uvicorn.develop")


class TrackManager:
    """
    Общие методы работы с треками.
    Обработка сырых данных, форматов, валидация первичная и тд.
    Некоторые базовые расчеты (расстояние между двумя точками).
    """

    RADIAN_COEFF = 0.01744  # Преобразуем радианы в градусы
    EARTH_RADIUS = 6371     # Радиус земли. Усредненный

    GPX_SCHEMA_GPX10 = BASE_DIR / "gps_test_files/gpx_strict.xsd"
    GPX_SCHEMA_GPX11 = BASE_DIR / "gps_test_files/gpx_strict2.xsd"
    GPX_SCHEMA_UPTRAIL = BASE_DIR / "gps_test_files/uptrail_custom.xsd"

    @classmethod
    def __get_format(cls, track: str) -> str:
        """Получаем формат файла."""
        split_name = track.filename.split('.')
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
        track = GPXTrack(track_file.file)
        return track

    def __gpx_validate(
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
            print("XML data is not valid.")
            os.remove(BASE_DIR / f"temp_{track_file.filename}")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "XML is not valid."
            )
        print("XML data is valid.")
        os.remove(BASE_DIR / f"temp_{track_file.filename}")
        track_file.file.seek(0)
        return True

    @classmethod
    def haversine_distance(
        cls, lat_start, long_start, lat_end, long_end
    ) -> float:
        distance = haversine(
            point1=(lat_start, long_start),
            point2=(lat_end, long_end),
            unit=Unit.METERS,
        )
        return distance


class GPXTrack:
    """
    Класс для обработки треков формата *.gpx.
    Получение общей информации, конвертация, обработка.
    """
    def __init__(self, file) -> None:
        self.__track = None
        self.__version: float = 0.0
        self.__start_latitude: float = None
        self.__start_longitude: float = None

        self.__tracks_amount: int = 0
        self.__segments_amount: int = 0
        self.__points_amount: int = 0

        self.__post_init_routine(file)

    def __post_init_routine(self, file: SpooledTemporaryFile):
        self.__track = gpxpy.parse(file)
        self.__version = self.__track.version
        if self.__version == "1.1":
            self.__tracks_amount = len(self.__track.tracks)
            self.__points_amount = self.__track.get_points_no()
            for i in range(self.__tracks_amount):
                self.__segments_amount += len(self.__track.tracks[i].segments)
        else:
            raise HTTPException(400, "Not supported version.")

    @classmethod
    def get_json_from_gpx(cls, file):
        """Преобразуем из gpx в json."""
        json_track = Converter(
            input_file=file).gpx_to_json(output_file="test.json")
        return json_track

    def is_empty(self) -> bool:
        return not self.__track.get_points_no() > 1

    def get_start_point(self) -> tuple[float, float]:
        """получение координаты стратовой точки трека."""
        if self.__track.version == "1.1" and not self.is_empty():
            self.__start_latitude = self.__track.tracks[0].segments[0].points[0].latitude
            self.__start_longitude = self.__track.tracks[0].segments[0].points[0].longitude
            return self.__start_latitude, self.__start_longitude
        if self.__track.version == "1.0" and not self.is_empty():
            self.__start_latitude = self.__track.waypoints[0].latitude
            self.__start_longitude = self.__track.waypoints[0].longitude
        else:
            raise HTTPException(400, "Wrong version or track is empty.")

    def get_total_distance(self) -> float:
        """Расчет общей дисатнции трека."""
        distance = 0
        for track in range(self.__tracks_amount):
            for segment in range(self.__segments_amount):
                for point_no, _ in enumerate(self.__track.tracks[track].segments[segment].points):
                    if point_no == 0:
                        continue
                    else:
                        distance += TrackManager.haversine_distance(
                            self.__track.tracks[track].segments[segment].points[point_no-1].latitude,
                            self.__track.tracks[track].segments[segment].points[point_no-1].longitude,
                            self.__track.tracks[track].segments[segment].points[point_no].latitude,
                            self.__track.tracks[track].segments[segment].points[point_no].longitude,
                        )
        return round(distance, 3)

    def get_general_info(self) -> tuple[float, float, float]:
        """Получаем информацию о треке."""
        return (
            self.get_start_point()[0],
            self.get_start_point()[1],
            self.get_total_distance(),
        )
