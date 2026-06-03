from uuid import UUID

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.rewards_schema import (
    RedeemRewardRequest
)

from app.services.rewards_service import (
    RewardsService
)

router = APIRouter(
    prefix="/customer/rewards",
    tags=["Customer Rewards"]
)


@router.get("/points")
async def get_reward_points(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await RewardsService.get_points(
        db,
        user_id
    )


@router.get("/progress")
async def get_reward_progress(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await RewardsService.get_progress(
        db,
        user_id
    )


@router.get("/history")
async def get_reward_history(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await RewardsService.get_history(
        db,
        user_id
    )


@router.post("/redeem")
async def redeem_reward(
    user_id: UUID,
    request: RedeemRewardRequest,
    db: AsyncSession = Depends(get_db)
):
    return await RewardsService.redeem_reward(
        db,
        user_id,
        request.reward_name,
        request.points_required
    )