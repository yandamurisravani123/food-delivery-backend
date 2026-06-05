from sqlalchemy import func, select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.restaurant import Restaurant
from app.models.review import Review


class FilterRepository:

    @staticmethod
    async def filter_restaurants(
        session: AsyncSession,
        cuisine: str = None,
        rating: float = None
    ):

        rating_expr = func.coalesce(func.avg(Review.rating), 0.0).label("avg_rating")

        if rating is not None:
            review_count_result = await session.execute(
                select(func.count(Review.id))
            )
            review_count = review_count_result.scalar_one()
            if review_count == 0:
                rating = None

        query = (
            select(Restaurant, rating_expr)
            .outerjoin(Review, Review.restaurant_id == Restaurant.id)
            .group_by(Restaurant.id)
        )

        if cuisine:
            query = query.where(
                Restaurant.cuisine_types.ilike(
                    f"%{cuisine}%"
                )
            )

        if rating:
            query = query.having(
                rating_expr >= rating
            )

        result = await session.execute(query)

        restaurants = result.all()

        return [
            {
                "id": str(restaurant.id),
                "restaurant_name": restaurant.restaurant_name,
                "cuisine_types": restaurant.cuisine_types,
                "rating": float(avg_rating) if avg_rating is not None else 0.0,
                "city": restaurant.city
            }
            for restaurant, avg_rating in restaurants
        ]