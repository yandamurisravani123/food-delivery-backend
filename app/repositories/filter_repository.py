from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant


class FilterRepository:

    @staticmethod
    async def filter_restaurants(
        session: AsyncSession,
        cuisine: str = None,
        rating: float = None
    ):

        query = select(Restaurant)

        if cuisine:

            query = query.where(
                Restaurant.cuisine_types.ilike(
                    f"%{cuisine}%"
                )
            )

        if rating:

            query = query.where(
                Restaurant.rating >= rating
            )

        result = await session.execute(query)

        restaurants = result.scalars().all()

        return [

            {
                "id": str(r.id),
                "restaurant_name": r.restaurant_name,
                "cuisine_types": r.cuisine_types,
                "rating": r.rating,
                "city": r.city
            }

            for r in restaurants
        ]