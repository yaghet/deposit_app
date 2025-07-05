from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


async_engine = create_async_engine(settings.async_database_url)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator that yields a SQLAlchemy AsyncSession.

    This function can be used as a dependency in FastAPI endpoints to provide
    a database session that is automatically cleaned up after the request.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session.

    """
    async with AsyncSessionLocal() as session:
        yield session
