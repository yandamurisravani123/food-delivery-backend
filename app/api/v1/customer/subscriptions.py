from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.subscriptions import SubscriptionService

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


@router.post("/subscribe/{plan_id}")
async def subscribe(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await SubscriptionService.subscribe(
        db,
        plan_id
    )


@router.get("/current")
async def current_subscription(
    db: AsyncSession = Depends(get_db)
):
    return await SubscriptionService.get_current_subscription(
        db
    )


@router.get("/history")
async def subscription_history(
    db: AsyncSession = Depends(get_db)
):
    return await SubscriptionService.get_subscription_history(
        db
    )


@router.delete("/{subscription_id}")
async def cancel_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await SubscriptionService.cancel_subscription(
        db,
        subscription_id
    )