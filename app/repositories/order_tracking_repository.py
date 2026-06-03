# app/repositories/order_tracking_repository.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.order_tracking import OrderTracking


class OrderTrackingRepository:

    @staticmethod
    async def get_order_tracking(
        db: AsyncSession,
        order_id
    ):
        query = (
            select(Order, OrderTracking)
            .join(
                OrderTracking,
                Order.id == OrderTracking.order_id
            )
            .where(Order.id == order_id)
        )

        result = await db.execute(query)

        return result.first()

    @staticmethod
    async def update_driver_location(
        db: AsyncSession,
        order_id,
        latitude,
        longitude
    ):
        query = select(OrderTracking).where(
            OrderTracking.order_id == order_id
        )

        result = await db.execute(query)

        tracking = result.scalar_one_or_none()

        if tracking:
            tracking.latitude = latitude
            tracking.longitude = longitude

            await db.commit()
            await db.refresh(tracking)

        return tracking