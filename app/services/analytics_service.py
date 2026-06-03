from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.order import Order


class AnalyticsService:

    @staticmethod
    async def get_order_summary(db: AsyncSession) -> dict:
        result = await db.execute(select(func.count(Order.id)))
        total_orders = result.scalar()
        return {"total_orders": total_orders}