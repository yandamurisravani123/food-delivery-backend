from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.cuisine import Cuisine


class CuisineService:

    @staticmethod
    async def get_cuisines(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Cuisine)
        )

        return result.scalars().all()