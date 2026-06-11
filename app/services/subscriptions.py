from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.plans import Plan
from app.models.subscriptions import Subscription


class SubscriptionService:

    @staticmethod
    async def subscribe(db: AsyncSession, plan_id: int):
        result = await db.execute(
            select(Plan).where(Plan.id == plan_id)
        )
        plan = result.scalar_one_or_none()

        if not plan:
            return None

        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=plan.duration_days)

        subscription = Subscription(
            selected_plan=plan.name,
            start_date=start_date,
            end_date=end_date,
            status="ACTIVE"
        )

        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)

        return subscription

    @staticmethod
    async def get_current_subscription(db: AsyncSession):
        result = await db.execute(
            select(Subscription).order_by(Subscription.id.desc())
        )
        return result.scalars().first()

    @staticmethod
    async def cancel_subscription(db: AsyncSession, subscription_id: int):
        result = await db.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )
        subscription = result.scalar_one_or_none()

        if not subscription:
            return None

        subscription.status = "CANCELLED"

        await db.commit()
        await db.refresh(subscription)

        return subscription

    @staticmethod
    async def get_subscription_history(db: AsyncSession):
        result = await db.execute(
            select(Subscription).order_by(Subscription.id.desc())
        )
        return result.scalars().all()