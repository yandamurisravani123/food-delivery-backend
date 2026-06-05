from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from app.models.restaurant import Restaurant





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