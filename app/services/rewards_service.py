from fastapi import HTTPException

from app.models.reward_redemption import RewardRedemption

from app.repositories.rewards_repository import (
    RewardsRepository
)


class RewardsService:

    @staticmethod
    async def get_points(
        db,
        user_id
    ):
        reward = await RewardsRepository.get_reward_points(
            db,
            user_id
        )

        if not reward:
            raise HTTPException(
                status_code=404,
                detail="Reward points not found"
            )

        return reward

    @staticmethod
    async def get_progress(
        db,
        user_id
    ):
        reward = await RewardsRepository.get_reward_points(
            db,
            user_id
        )

        if not reward:
            raise HTTPException(
                status_code=404,
                detail="Reward points not found"
            )

        return {
            "current_points": reward.current_points,
            "target_points": reward.target_points,
            "remaining_points":
                reward.target_points -
                reward.current_points
        }

    @staticmethod
    async def get_history(
        db,
        user_id
    ):
        return await RewardsRepository.get_reward_history(
            db,
            user_id
        )

    @staticmethod
    async def redeem_reward(
        db,
        user_id,
        reward_name,
        points_required
    ):
        reward = await RewardsRepository.get_reward_points(
            db,
            user_id
        )

        if not reward:
            raise HTTPException(
                status_code=404,
                detail="Reward points not found"
            )

        if reward.current_points < points_required:
            raise HTTPException(
                status_code=400,
                detail="Insufficient reward points"
            )

        reward.current_points -= points_required

        redemption = RewardRedemption(
            user_id=user_id,
            reward_name=reward_name,
            points_used=points_required
        )

        return await RewardsRepository.create_redemption(
            db,
            redemption
        )