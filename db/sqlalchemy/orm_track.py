import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.tracks.models import Base, TrackModel
from config import settings

track_engine = create_async_engine(
    url=settings.database_url_async_psycopg,
    echo=True,
)

track_session = async_sessionmaker(bind=track_engine)


async def test_case_del_and_create():
    """utility function for deleting and creating a table in the database."""
    async with track_engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
        await connect.run_sync(Base.metadata.create_all)


async def add_track(model_instance, session=track_session):
    """create one record."""
    async with session() as async_session:
        async_session.add(model_instance)
        await async_session.commit()


async def show_all_tracks(session=track_session):
    """get all records."""
    async with session() as async_session:
        stmt = select(TrackModel)
        result = await async_session.execute(stmt)
        tracks = result.scalars().all()
        for track in tracks:
            print(track.name, track.description, track.author)


test_obj_track = TrackModel(
    name="test_track",
    description="test description more than 30 characters long",
    author="test_author",
    latitude_start=60.00562,
    longitude_start=30.69284,
    actual_route_length=22.25,
)
