from sqlalchemy import select

from .models import TrackModel
from database import track_session


async def add_track(
    model_instance,
    lt_lat,
    lt_long,
    rb_lat,
    rb_long,
    session=track_session
):
    """Add new track ro database."""
    async with session() as async_session:
        async_session.add(model_instance)
        await async_session.commit()


async def get_all_tracks(
    lt_lat, lt_long, rb_lat, rb_long, session=track_session
):
    """Get all records from database."""
    async with session() as async_session:
        query = select(TrackModel)
        result = await async_session.execute(query)
        tracks = result.scalars().all()
        return tracks
