from app.repositories.premium_repository import (
    PremiumRepository
)

from app.utils.qr_generator import (
    generate_qr
)


class PremiumService:

    @staticmethod
    async def get_card(
        db,
        user_id,
        user_name
    ):

        membership = await PremiumRepository.get_membership(
            db,
            user_id
        )

        qr_code = generate_qr(
            membership.member_code
        )

        return {
            "member_code": membership.member_code,
            "member_name": user_name,
            "member_since": membership.member_since,
            "qr_code": qr_code
        }

    @staticmethod
    async def get_benefits(db):

        return await PremiumRepository.get_benefits(db)

    @staticmethod
    async def get_status(
        db,
        user_id
    ):

        membership = await PremiumRepository.get_membership(
            db,
            user_id
        )

        return {
            "is_active": membership.is_active,
            "plan_name": membership.plan_name,
            "next_billing_date": membership.next_billing_date
        }

    @staticmethod
    async def get_points(
        db,
        user_id
    ):

        points = await PremiumRepository.get_reward_points(
            db,
            user_id
        )

        return {
            "current_points": points.current_points,
            "target_points": points.target_points
        }