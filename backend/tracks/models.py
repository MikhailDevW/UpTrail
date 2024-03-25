from sqlalchemy import (
    Integer, TEXT, FLOAT, JSON, String,
    TIMESTAMP, PrimaryKeyConstraint,
    UniqueConstraint, DATE
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Track(Base):

    __tablename__ = "track",

    id: Mapped[int] = mapped_column(Integer, primary_key=True),
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
        ),
    description: Mapped[str] = mapped_column(
        TEXT(15000), nullable=False
        ),
    datetime_start: Mapped[DATE] = mapped_column(TIMESTAMP.timezone),
    author: Mapped[str] = mapped_column(String(100), nullable=False),
    latitude_start: Mapped[float] = mapped_column(FLOAT),
    longitude_start: Mapped[float] = mapped_column(FLOAT),
    actual_route_length: Mapped[str] = mapped_column(String(100)),
    gps_file: Mapped[JSON] = mapped_column(JSON, nullable=True)

    __table_args__ = (
            PrimaryKeyConstraint("id", name="track_id"),
            UniqueConstraint(
                "name", "author", name="uq_user_fields"
                ),
        )
