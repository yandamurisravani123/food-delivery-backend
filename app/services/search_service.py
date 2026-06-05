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

        stmt = (
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
                    Restaurant.restaurant_name.ilike(f"%{keyword}%"),
                    Restaurant.city.ilike(f"%{keyword}%")
                )
            )
        )

        result = await db.execute(stmt)

        restaurants = result.scalars().all()

        return {
            "success": True,
            "count": len(restaurants),
            "data": [
                {
                    "id": str(r.id),
                    "restaurant_name": r.restaurant_name,
                    "city": r.city
                }
                for r in restaurants
            ]
        }