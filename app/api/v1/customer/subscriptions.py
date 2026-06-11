from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
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
    result = await SubscriptionService.subscribe(db, plan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Plan not found")
    return result


@router.get("/current")
async def current_subscription(
    db: AsyncSession = Depends(get_db)
):
    result = await SubscriptionService.get_current_subscription(db)
    if not result:
        raise HTTPException(status_code=404, detail="No active subscription found")
    return result


@router.get("/history")
async def subscription_history(
    db: AsyncSession = Depends(get_db)
):
    return await SubscriptionService.get_subscription_history(db)


@router.delete("/{subscription_id}")
async def cancel_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await SubscriptionService.cancel_subscription(db, subscription_id)
    if not result:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return result