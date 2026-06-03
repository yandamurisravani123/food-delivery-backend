# app/services/savings_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.savings import UserSavings


class SavingsService:

    # -------------------------
    # GET USER SAVINGS
    # -------------------------
    @staticmethod
    async def get_user_savings(user_id: int, db: AsyncSession):
        result = await db.execute(
            select(UserSavings).where(UserSavings.user_id == user_id)
        )
        return result.scalar_one_or_none()

    # -------------------------
    # CALCULATIONS
    # -------------------------
    @staticmethod
    def calculate_progress(monthly_saved, monthly_goal):
        if monthly_goal == 0:
            return 0
        return round((monthly_saved / monthly_goal) * 100, 2)

    @staticmethod
    def remaining_amount(monthly_saved, monthly_goal):
        return max(monthly_goal - monthly_saved, 0)

    # -------------------------
    # TIER LOGIC
    # -------------------------
    @staticmethod
    def get_tier_info(total_saved: float, percentile: float):

        if total_saved >= 500:
            return {
                "tier": "Gold",
                "next_tier": "Platinum",
                "amount_to_next_tier": max(1000 - total_saved, 0)
            }

        elif total_saved >= 200:
            return {
                "tier": "Silver",
                "next_tier": "Gold",
                "amount_to_next_tier": max(500 - total_saved, 0)
            }

        else:
            return {
                "tier": "Bronze",
                "next_tier": "Silver",
                "amount_to_next_tier": max(200 - total_saved, 0)
            }

    # -------------------------
    # BUILD RESPONSE
    # -------------------------
    @staticmethod
    async def build_overview(user_id: int, db: AsyncSession):

        data = await SavingsService.get_user_savings(user_id, db)

        # default if no record
        if not data:
            return {
                "total_saved": 0,
                "breakdown": {
                    "delivery_fee_saved": 0,
                    "discount_saved": 0,
                    "wallet_credit_saved": 0
                },
                "monthly_goal": 100,
                "monthly_saved": 0,
                "progress_percent": 0,
                "remaining_to_goal": 100,
                "tier_info": {
                    "tier": "Bronze",
                    "percentile": 0,
                    "next_tier": "Silver",
                    "amount_to_next_tier": 200
                }
            }

        progress = SavingsService.calculate_progress(
            data.monthly_saved,
            data.monthly_goal
        )

        remaining = SavingsService.remaining_amount(
            data.monthly_saved,
            data.monthly_goal
        )

        tier = SavingsService.get_tier_info(
            data.total_saved,
            data.percentile
        )

        return {
            "total_saved": data.total_saved,
            "breakdown": {
                "delivery_fee_saved": data.delivery_fee_saved,
                "discount_saved": data.discount_saved,
                "wallet_credit_saved": data.wallet_credit_saved
            },
            "monthly_goal": data.monthly_goal,
            "monthly_saved": data.monthly_saved,
            "progress_percent": progress,
            "remaining_to_goal": remaining,
            "tier_info": {
                "tier": tier["tier"],
                "percentile": data.percentile,
                "next_tier": tier["next_tier"],
                "amount_to_next_tier": tier["amount_to_next_tier"]
            }
        }