from collections.abc import AsyncGenerator
from typing import Any, TypeVar

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

T = TypeVar("T", bound="Base")

engine = create_async_engine(settings.database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    @classmethod
    async def create(cls: type[T], session: AsyncSession, **kwargs: Any) -> T:
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def get_by_id(
        cls: type[T], session: AsyncSession, obj_id: Any
    ) -> T | None:
        return await session.get(cls, obj_id)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
