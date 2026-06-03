from sqlalchemy.future import select

from app.models.review import Review


class ReviewRepository:

    @staticmethod
    async def create_review(
        db,
        review
    ):

        db.add(review)

        await db.commit()

        await db.refresh(review)

        return review


    @staticmethod
    async def get_review_by_order(
        db,
        order_id
    ):

        result = await db.execute(
            select(Review).where(
                Review.order_id == order_id
            )
        )

        return result.scalar_one_or_none()