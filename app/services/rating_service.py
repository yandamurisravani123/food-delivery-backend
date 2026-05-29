from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.ratings import Rating


class RatingService:

    @staticmethod
    async def create_rating(
        db: AsyncSession,
        data
    ):

        rating = Rating(
            customer_id=data.customer_id,
            driver_id=data.driver_id,
            order_id=data.order_id,
            rating=data.rating,
            feedback_tags=",".join(
                data.feedback_tags
            ) if data.feedback_tags else None,
            review=data.review
        )

        db.add(rating)

        await db.commit()
        await db.refresh(rating)

        return rating

    @staticmethod
    async def get_driver_ratings(
        db: AsyncSession,
        driver_id: int
    ):

        result = await db.execute(
            select(Rating).where(
                Rating.driver_id == driver_id
            )
        )

        return result.scalars().all()