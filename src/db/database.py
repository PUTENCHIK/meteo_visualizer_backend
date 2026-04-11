from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/meteo_visualizer"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with async_session() as session:
        yield session
