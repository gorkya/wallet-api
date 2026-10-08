import pytest
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.database import Base
from app.config import settings
from app.models import Wallet


TEST_DATABASE_URL = settings.test_database_url


@pytest.fixture
async def engine():
    if TEST_DATABASE_URL is None:
        pytest.fail("TEST_DATABASE_URL is not set")

    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def session(session_maker):
    async with session_maker() as session:
        yield session


@pytest.fixture
async def wallet(session):
    wallet = await Wallet.create(session)
    await session.commit()
    return wallet