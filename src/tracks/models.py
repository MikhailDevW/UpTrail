from sqlalchemy import (
    DATE, FLOAT, JSON, CheckConstraint, PrimaryKeyConstraint, String,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.database import Base

MIN_NAME_LEN: int = 7
MAX_NAME_LEN: int = 255
MIN_DESC_LEN: int = 30
MAX_DESC_LEN: int = 10000
MIN_AUTHOR_LEN: int = 7
MAX_AUTHOR_LEN: int = 255

MIN_ROUTE_VALUE: int = 0
MAX_ROUTE_VALUE: int = 200000


class TrackModel(Base):
    """
    Модель для отслеживания треков.
    Attributes:
    - id: уникальный идентификатор трека
    - name: название трека
    - description: описание трека
    - author: автор трека
    - datetime_start: время начала трека
    - latitude_start: широта начальной точки
    - longitude_start: долгота начальной точки
    - actual_route_length: фактическая длина маршрута
    """

    __tablename__ = "track"

    name: Mapped[str] = mapped_column(
        String(MAX_NAME_LEN), nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(MAX_DESC_LEN), nullable=False,
    )
    datetime_start: Mapped[DATE] = mapped_column(DATE, nullable=True)
    author: Mapped[str] = mapped_column(
        String(MAX_AUTHOR_LEN), nullable=False,
    )
    latitude_start: Mapped[float] = mapped_column(FLOAT, nullable=True)
    longitude_start: Mapped[float] = mapped_column(FLOAT, nullable=True)
    actual_route_length: Mapped[float] = mapped_column(FLOAT, nullable=True)
    gps_file: Mapped[JSON] = mapped_column(JSON, nullable=True)

    @validates("name")
    def validate_name(self, key, name: str) -> str:
        if not name:
            raise ValueError("The name cannot be empty!")
        if len(name) < MIN_NAME_LEN:
            raise ValueError(
                f"Minimum name length {MIN_NAME_LEN} characters"
            )
        if len(name) > MAX_NAME_LEN:
            raise ValueError(
                f"Maximum name length {MAX_NAME_LEN} characters"
            )

        return name

    @validates("description")
    def validate_description(self, key, description: str) -> str:
        if not description:
            raise ValueError("The description cannot be empty!")
        if len(description) < MIN_DESC_LEN:
            raise ValueError(
                f"Minimum description length {MIN_DESC_LEN} characters"
            )
        if len(description) > MAX_DESC_LEN:
            raise ValueError(
                f"Maximum description length {MAX_DESC_LEN} characters"
            )

        return description

    @validates("author")
    def validate_author(self, key, author: str) -> str:
        if not author:
            raise ValueError("The author cannot be empty!")
        if len(author) < MIN_AUTHOR_LEN:
            raise ValueError(
                f"Minimum author length {MIN_AUTHOR_LEN} characters"
            )
        if len(author) > MAX_AUTHOR_LEN:
            raise ValueError(
                f"Maximum author length {MAX_AUTHOR_LEN} characters"
            )

        return author

    @validates("latitude_start")
    def validate_latitude_start(self, key, latitude_start: float) -> float:
        if not latitude_start:
            raise ValueError("The latitude_start cannot be empty!")
        if latitude_start < -90:
            raise ValueError(
                "The value must be greater than minus 90"
            )
        if latitude_start > 90:
            raise ValueError(
                "The value cannot be greater than 90"
            )

        return latitude_start

    @validates("longitude_start")
    def validate_longitude_start(self, key, longitude_start: float) -> float:
        if not longitude_start:
            raise ValueError("The longitude_start cannot be empty!")
        if longitude_start < -180:
            raise ValueError(
                "The value must be greater than minus -180"
            )
        if longitude_start > 180:
            raise ValueError(
                "The value cannot be greater than 180"
            )

        return longitude_start

    @validates("actual_route_length")
    def validate_actual_route_length(
        self, key, actual_route_length: float
    ) -> float:
        """Value in km."""

        if actual_route_length <= MIN_ROUTE_VALUE:
            raise ValueError(
                f"The value must be greater than {MIN_ROUTE_VALUE}"
            )
        if actual_route_length > MAX_ROUTE_VALUE:
            raise ValueError(
                f"The value cannot be greater than {MAX_ROUTE_VALUE}"
            )
        return actual_route_length

    @validates("gps_file")
    def validate_gps_file(self, key, gps_file):
        if not gps_file:
            raise ValueError("The gps_file cannot be empty!")
        return gps_file

    __table_args__ = (
        PrimaryKeyConstraint("id"),
        UniqueConstraint(
            "name", "author", "datetime_start", name="uq_track"
        ),
        CheckConstraint(
            f"LENGTH(name) >= {MIN_NAME_LEN} AND"
            f" LENGTH(name) <= {MAX_NAME_LEN}",
            name="check_name_length"
        ),
        CheckConstraint(
            f"LENGTH(description) >= {MIN_DESC_LEN} AND"
            f" LENGTH(description) <= {MAX_DESC_LEN}",
            name="check_description_length"
        ),
        CheckConstraint(
            f"LENGTH(author) >= {MIN_AUTHOR_LEN} AND"
            f" LENGTH(author) <= {MAX_AUTHOR_LEN}",
            name="check_author_length"
        ),
        CheckConstraint(
            "latitude_start >= -90 AND latitude_start <= 90",
            name="check_latitude_start_range"
        ),
        CheckConstraint(
            "longitude_start >= -180 AND longitude_start <= 180",
            name="check_longitude_start_range"
        ),
        CheckConstraint(
            f"actual_route_length > {MIN_ROUTE_VALUE} AND"
            f" actual_route_length <= {MAX_ROUTE_VALUE}",
            name="check_actual_route_length_range"
        ),
    )
