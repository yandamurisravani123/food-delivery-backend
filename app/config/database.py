from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings


# DATABASE ENGINE
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)


# ASYNC SESSION FACTORY
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# BASE MODEL
class Base(DeclarativeBase):
    pass


# DATABASE DEPENDENCY
async def get_db():

    async with AsyncSessionLocal() as session:
        yield session