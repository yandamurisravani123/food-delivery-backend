from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ratings import Rating
from app.schemas.ratings_schema import RatingCreate


class RatingService:

    @staticmethod
    async def create_rating(
        db: AsyncSession,
        payload: RatingCreate
    ):

        new_rating = Rating(
            customer_id=payload.customer_id,
            driver_id=payload.driver_id,
            order_id=payload.order_id,
            rating=payload.rating,
            feedback=payload.feedback,
            tag=payload.tag
        )

        db.add(new_rating)
        await db.commit()
        await db.refresh(new_rating)

        return new_rating

    @staticmethod
    async def get_all_ratings(
        db: AsyncSession
    ):
        query = select(Rating)

        result = await db.execute(query)

        return result.scalars().all()