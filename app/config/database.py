from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker , AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings
#from app.config.database import engine

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session