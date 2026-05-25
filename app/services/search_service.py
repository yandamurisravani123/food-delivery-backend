from sqlalchemy import select

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.restaurant import (
    Restaurant
)

# ==========================================
# ADD THIS IMPORT
# ==========================================

from app.repositories.search_repository import (
    SearchRepository
)


class SearchService:

    @staticmethod
    async def search_restaurants(
        keyword: str,
        db: AsyncSession
    ):

        # ==========================================
        # OLD CODE
        # ==========================================

        result = await db.execute(
            select(Restaurant).where(
                Restaurant.restaurant_name.ilike(
                    f"%{keyword}%"
                )
            )
        )

        restaurants = result.scalars().all()

        # ==========================================
        # ADD THIS RETURN FORMAT
        # ==========================================

        return {
            "success": True,
            "message": "Search results fetched successfully",
            "data": restaurants
        }