from sqlalchemy import select

from app.models.membership import Membership
from app.models.membership_benefit import MembershipBenefit
from app.models.reward_point import RewardPoint


class PremiumRepository:

    @staticmethod
    async def get_membership(db, user_id):

        result = await db.execute(
            select(Membership)
            .where(Membership.user_id == user_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_benefits(db):

        result = await db.execute(
            select(MembershipBenefit)
        )

        return result.scalars().all()

    @staticmethod
    async def get_reward_points(db, user_id):

        result = await db.execute(
            select(RewardPoint)
            .where(RewardPoint.user_id == user_id)
        )

        return result.scalar_one_or_none()