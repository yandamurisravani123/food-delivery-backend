from sqlalchemy import select

from app.models.reward_point import RewardPoint
from app.models.reward_transaction import RewardTransaction
from app.models.reward_redemption import RewardRedemption


class RewardsRepository:

    @staticmethod
    async def get_reward_points(
        db,
        user_id
    ):
        result = await db.execute(
            select(RewardPoint).where(
                RewardPoint.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_reward_history(
        db,
        user_id
    ):
        result = await db.execute(
            select(RewardTransaction).where(
                RewardTransaction.user_id == user_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def create_redemption(
        db,
        redemption
    ):
        db.add(redemption)

        await db.commit()

        await db.refresh(redemption)

        return redemption