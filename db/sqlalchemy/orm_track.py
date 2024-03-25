import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))


from sqlalchemy import create_engine

from backend.tracks.models import Base
from config import settings

track_engine = create_engine(
    url=settings.DatabaseUrlPsycopg,
    echo=True,
    pool_size=3
)


def delete_tabl():
    Base.metadata.drop_all(track_engine)
    track_engine.echo = True


def create_tabl():
    Base.metadata.create_all(track_engine)
    track_engine.echo = True

delete_tabl()
create_tabl()