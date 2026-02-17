from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from env import _env

ASYNC_DATABASE_URL = _env.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


engine = create_async_engine(ASYNC_DATABASE_URL, echo=_env.DEBUG, future=True)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session
