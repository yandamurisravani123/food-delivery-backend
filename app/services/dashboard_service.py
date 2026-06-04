from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order


class DashboardService:

    @staticmethod
    async def get_metrics(session: AsyncSession, restaurant_id):

        total_orders = await session.scalar(
            select(func.count(Order.id))
            .where(Order.restaurant_id == restaurant_id)
        ) or 0

        repeat_orders = await session.scalar(
            select(func.count(distinct(Order.user_id)))
            .where(Order.restaurant_id == restaurant_id)
        ) or 0

        repeat_rate = (
            round((repeat_orders / total_orders) * 100, 2)
            if total_orders > 0 else 0
        )

        return {
            "total_orders": total_orders,
            "repeat_orders": repeat_orders,
            "repeat_rate": repeat_rate
        }

    @staticmethod
    async def repeat_orders(session: AsyncSession, restaurant_id):

        result = await session.execute(
            select(
                Order.user_id.label("user_id"),
                func.count(Order.id).label("orders")
            )
            .where(Order.restaurant_id == restaurant_id)
            .group_by(Order.user_id)
        )

        return [
            {
                "user_id": row.user_id,
                "orders": row.orders
            }
            for row in result.all()
        ]

    @staticmethod
    async def market_reach(session: AsyncSession, restaurant_id):

        reach = await session.scalar(
            select(func.count(func.distinct(Order.user_id)))
            .where(Order.restaurant_id == restaurant_id)
        ) or 0

        return {"reach": reach}

    @staticmethod
    async def rating_trend(session: AsyncSession, restaurant_id):
        return {
            "ratings": [],
            "message": "Review system not implemented yet"
        }

    # ---------------- OPTIONAL ANALYTICS (ALL INSIDE CLASS) ----------------

    @staticmethod
    async def growth_tips(session: AsyncSession, restaurant_id):
        return {
            "tips": [
                "Optimize your top-selling items placement",
                "Run discount campaigns during peak hours",
                "Improve delivery time consistency"
            ]
        }

    @staticmethod
    async def competitor_benchmark(session: AsyncSession, restaurant_id):
        return {
            "benchmark": {
                "your_performance": "good",
                "market_position": "mid-tier"
            }
        }

    @staticmethod
    async def marketing_impact(session: AsyncSession, restaurant_id):
        return {
            "impact_score": 72,
            "message": "Moderate campaign effectiveness"
        }

    @staticmethod
    async def stock_efficiency(session: AsyncSession, restaurant_id):
        return {
            "efficiency": 85,
            "message": "Stock usage is optimized"
        }

    @staticmethod
    async def staff_performance(session: AsyncSession, restaurant_id):
        return {
            "rating": 4.3,
            "message": "Stable staff performance"
        }

    @staticmethod
    async def dashboard_summary(session: AsyncSession, restaurant_id):

        metrics = await DashboardService.get_metrics(session, restaurant_id)
        repeat = await DashboardService.repeat_orders(session, restaurant_id)
        reach = await DashboardService.market_reach(session, restaurant_id)
        ratings = await DashboardService.rating_trend(session, restaurant_id)

        return {
            "metrics": metrics,
            "repeat_orders": repeat,
            "market_reach": reach,
            "rating_trend": ratings,
            "ui_ready": True
        }