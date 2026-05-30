from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.driver import Driver


class DriverService:

    @staticmethod
    async def get_all_drivers(
        session: AsyncSession
    ):
        result = await session.execute(
            select(Driver)
        )
        return result.scalars().all()

    @staticmethod
    async def get_driver_by_id(
        session: AsyncSession,
        driver_id: int
    ):
        result = await session.execute(
            select(Driver).where(
                Driver.id == driver_id
            )
        )
        return result.scalar_one_or_none()