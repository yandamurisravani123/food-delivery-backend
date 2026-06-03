from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.map_repository import (
    MapRepository
)


class MapService:

    @staticmethod
    async def get_restaurants(
        session: AsyncSession
    ):

        restaurants = await MapRepository.get_restaurants(
            session
        )

        return {
            "success": True,
            "message": "Map restaurants fetched successfully",
            "data": restaurants
        }