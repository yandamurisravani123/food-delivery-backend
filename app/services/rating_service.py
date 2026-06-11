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

    # Alias for create_rating
    @staticmethod
    async def create_review(
        db: AsyncSession,
        payload: RatingCreate
    ):
        return await RatingService.create_rating(db, payload)

    @staticmethod
    async def get_all_ratings(
        db: AsyncSession
    ):
        result = await db.execute(select(Rating))
        return result.scalars().all()

    @staticmethod
    async def get_order_review(
        db: AsyncSession,
        order_id
    ):
        result = await db.execute(
            select(Rating).where(Rating.order_id == order_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_driver_reviews(
        db: AsyncSession,
        driver_id
    ):
        result = await db.execute(
            select(Rating).where(Rating.driver_id == driver_id)
        )
        return result.scalars().all()