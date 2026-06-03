from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant


class SearchRepository:

    @staticmethod
    async def search_restaurants(
        session: AsyncSession,
        query: str
    ):

        result = await session.execute(
            select(Restaurant).where(
                Restaurant.restaurant_name.ilike(
                    f"%{query}%"
                )
            )
        )

        return result.scalars().all()