from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.filter_repository import (
    FilterRepository
)


class FilterService:

    @staticmethod
    async def filter_restaurants(
        session: AsyncSession,
        cuisine: str = None,
        rating: float = None
    ):

        restaurants = await FilterRepository.filter_restaurants(
            session,
            cuisine,
            rating
        )

        return {
            "success": True,
            "message": "Filtered restaurants fetched successfully",
            "data": restaurants
        }