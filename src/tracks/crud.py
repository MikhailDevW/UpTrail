from sqlalchemy import select

from src.database import async_session

from .models import TrackModel


async def add_track(
    model_instance,
    lt_lat,
    lt_long,
    rb_lat,
    rb_long,
    session=async_session
):
    """Add new track ro database."""
    async with session() as async_session:
        async_session.add(model_instance)
        await async_session.commit()


async def get_all_tracks(
    lt_lat, lt_long, rb_lat, rb_long, session=async_session
):
    """Get all records from database."""
    async with session() as async_session:
        query = select(TrackModel)
        result = await async_session.execute(query)
        tracks = result.scalars().all()
        return tracks
