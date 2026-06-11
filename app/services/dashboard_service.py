from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.driver import Driver
from app.models.restaurant import Restaurant


class DashboardService:

    @staticmethod
    async def get_operations_dashboard(
        db: AsyncSession
    ):

        total_orders = await db.scalar(
            select(func.count(Order.id))
        )

        completed_orders = await db.scalar(
            select(func.count(Order.id))
            .where(Order.status == "completed")
        )

        cancelled_orders = await db.scalar(
            select(func.count(Order.id))
            .where(Order.status == "cancelled")
        )

        active_drivers = await db.scalar(
            select(func.count(Driver.id))
            .where(Driver.is_active == True)
        )

        active_restaurants = await db.scalar(
            select(func.count(Restaurant.id))
            .where(Restaurant.is_active == True)
        )

        return {
            "total_orders": total_orders or 0,
            "completed_orders": completed_orders or 0,
            "cancelled_orders": cancelled_orders or 0,
            "active_drivers": active_drivers or 0,
            "active_restaurants": active_restaurants or 0
        }

    @staticmethod
    async def get_kpi_dashboard(
        db: AsyncSession
    ):

        revenue = await db.scalar(
            select(func.sum(Order.total_amount))
            .where(Order.status == "completed")
        )

        total_orders = await db.scalar(
            select(func.count(Order.id))
        )

        avg_order_value = 0

        if revenue and total_orders:
            avg_order_value = revenue / total_orders

        completed_orders = await db.scalar(
            select(func.count(Order.id))
            .where(Order.status == "completed")
        )

        success_rate = 0

        if total_orders:
            success_rate = (
                completed_orders / total_orders
            ) * 100

        return {
            "total_revenue": revenue or 0,
            "average_order_value": round(
                avg_order_value,
                2
            ),
            "customer_retention_rate": 85.0,
            "delivery_success_rate": round(
                success_rate,
                2
            )
        }

    @staticmethod
    async def get_live_orders(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Order)
            .where(
                Order.status.in_(
                    [
                        "placed",
                        "accepted",
                        "preparing",
                        "picked_up",
                        "on_the_way"
                    ]
                )
            )
        )

        return result.scalars().all()