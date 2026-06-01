from sqlalchemy import select
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from app.models.restaurant import Restaurant

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.restaurant import (
    Restaurant
)





from app.repositories.search_repository import (
    SearchRepository
)


# class SearchService:

#     @staticmethod
#     async def search_restaurants(
#         keyword: str,
#         db: AsyncSession
#     ):

        # ==========================================
        # OLD CODE
        # ==========================================

        # result = await db.execute(
        #     select(Restaurant).where(
        #         Restaurant.restaurant_name.ilike(
        #             f"%{keyword}%"
        #         )
        #     )
        # )

        # restaurants = result.scalars().all()

        # ==========================================
        # ADD THIS RETURN FORMAT
        # ==========================================

        # return {
        #     "success": True,
        #     "message": "Search results fetched successfully",
        #     "data": restaurants
        # }

class SearchService:

    @staticmethod
    async def search_restaurants(
        keyword: str,
        db: AsyncSession
    ):

        try:

            result = await db.execute(
                select(Restaurant).where(
                    or_(
                        Restaurant.restaurant_name.ilike(
                            f"%{keyword}%"
                        ),
                        Restaurant.city.ilike(
                            f"%{keyword}%"
                        )
                    )
                )
            )

            restaurants = result.scalars().all()

            return {
                "success": True,
                "message": "Search results fetched successfully",
                "count": len(restaurants),
                "data": [
                    {
                        "id": restaurant.id,
                        "restaurant_name": restaurant.restaurant_name,
                        "city": restaurant.city
                    }
                    for restaurant in restaurants
                ]
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }
class SearchService:

    @staticmethod
    async def search_restaurants(
        keyword: str,
        db: AsyncSession
    ):

        query = (
            select(Restaurant)
            .options(
            load_only(
                    Restaurant.id,
                    Restaurant.restaurant_name,
                    Restaurant.city
                )
            )
            .where(
                or_(
                    Restaurant.restaurant_name.ilike(
                        f"%{keyword}%"
                    ),
                    Restaurant.city.ilike(
                        f"%{keyword}%"
                    )
                )
            )
        )

        result = await db.execute(query)

        restaurants = result.scalars().all()

        return {
            "success": True,
            "count": len(restaurants),
            "data": [
                {
                    "id": restaurant.id,
                    "restaurant_name": restaurant.restaurant_name,
                    "city": restaurant.city
                }
                for restaurant in restaurants
            ]
        }