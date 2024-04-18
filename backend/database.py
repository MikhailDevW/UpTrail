import asyncio

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASSWORD


class Base(DeclarativeBase):
    pass


def database_url_async():
    return (
        f"postgresql+asyncpg:"
        f"//{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


async_engine = create_async_engine(
    url=database_url_async(),
    echo=True,
    pool_size=5,
)


track_session = async_sessionmaker(bind=async_engine)


async def get_db_version():
    async with async_engine.connect() as db_connection:
        res = await db_connection.execute(text("SELECT VERSION()"))
        print(res.all())


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
        stmt = select(TrackModel)
        result = await async_session.execute(stmt)
        tracks = result.scalars().all()
        return tracks

# test cases
if __name__ == "__main__":
    async def test_case_del_and_create():
        async with async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.drop_all)
            # await connect.run_sync(Base.metadata.create_all)

    asyncio.run(test_case_del_and_create())
