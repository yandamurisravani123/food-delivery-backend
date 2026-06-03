from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.order import Order, OrderStatus


class OrderService:

    @staticmethod
    async def get_order_by_id(db: AsyncSession, order_id: int):
        result = await db.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_orders_by_user(db: AsyncSession, user_id):
        result = await db.execute(
            select(Order).where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update_order_status(db: AsyncSession, order_id: int, status: OrderStatus):
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order:
            order.status = status.value
            await db.commit()
            await db.refresh(order)
        return order