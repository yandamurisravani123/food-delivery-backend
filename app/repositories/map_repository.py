from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant


class MapRepository:

    @staticmethod
    async def get_restaurants(
        session: AsyncSession
    ):

        result = await session.execute(
            select(Restaurant)
        )

        return result.scalars().all()