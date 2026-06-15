from unittest import result

from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order, OrderStatus
from app.models.payment import Payment
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.delivery import DeliveryAgent
from datetime import datetime, timezone
from app.schemas.dashboard import (
    OperationsDashboardResponse,
    BusinessKPIDashboardResponse,
    LiveOrder,
    LiveOrdersDashboardResponse,
)



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


    # ======================================================
    # OPERATIONS DASHBOARD
    # ======================================================


    @staticmethod
    async def get_overview(db):
        # existing code
        ...

    @staticmethod
    async def get_operations_dashboard(db):
        # write your operations dashboard logic here
        ...
    @staticmethod
    async def operations_dashboard(
        db: AsyncSession,
    ) -> OperationsDashboardResponse:

        total_orders = await db.scalar(
            select(func.count(Order.id))
        ) or 0

        pending_orders = await db.scalar(
            select(func.count(Order.id)).where(
                Order.status == OrderStatus.pending
            )
        ) or 0

        accepted_orders = await db.scalar(
            select(func.count(Order.id)).where(
                Order.status == OrderStatus.accepted
            )
        ) or 0

        preparing_orders = await db.scalar(
            select(func.count(Order.id)).where(
                Order.status == OrderStatus.preparing
            )
        ) or 0

        out_for_delivery = await db.scalar(
            select(func.count(Order.id)).where(
                Order.status == OrderStatus.out_for_delivery
            )
        ) or 0

        completed_orders = await db.scalar(
            select(func.count(Order.id)).where(
                Order.status == OrderStatus.completed
            )
        ) or 0

        cancelled_orders = await db.scalar(
            select(func.count(Order.id)).where(
                Order.status == OrderStatus.cancelled
            )
        ) or 0

        total_customers = await db.scalar(
            select(func.count(User.id))
        ) or 0

        total_drivers = await db.scalar(
            select(func.count(DeliveryAgent.id))
        ) or 0

        active_drivers = await db.scalar(
            select(func.count(DeliveryAgent.id)).where(
                DeliveryAgent.is_available == True
            )
        ) or 0

        offline_drivers = total_drivers - active_drivers

        total_restaurants = await db.scalar(
            select(func.count(Restaurant.id))
        ) or 0

        return OperationsDashboardResponse(
            total_orders=total_orders,
            pending_orders=pending_orders,
            accepted_orders=accepted_orders,
            preparing_orders=preparing_orders,
            out_for_delivery=out_for_delivery,
            completed_orders=completed_orders,
            cancelled_orders=cancelled_orders,
            total_customers=total_customers,
            total_drivers=total_drivers,
            active_drivers=active_drivers,
            offline_drivers=offline_drivers,
            total_restaurants=total_restaurants,
        )

    # ======================================================
    # BUSINESS KPI DASHBOARD
    # ======================================================

    @staticmethod
    async def get_business_kpi_dashboard(db):
        total_revenue = await db.scalar(
            select(func.coalesce(func.sum(Payment.amount), 0))
            .where(Payment.status == "Completed")
        )

        today_revenue = await db.scalar(
            select(func.coalesce(func.sum(Payment.amount), 0))
            .where(Payment.status == "Completed")
        )

        monthly_revenue = today_revenue

        total_orders = await db.scalar(
            select(func.count(Order.id))
        ) or 0

        average_order_value = (
            total_revenue / total_orders
            if total_orders > 0 else 0
        )

        total_refunds = 0

        platform_commission = total_revenue * 0.10

        customer_growth = 0
        driver_growth = 0
        restaurant_growth = 0

        return {
            "total_revenue": float(total_revenue),
            "today_revenue": float(today_revenue),
            "monthly_revenue": float(monthly_revenue),
            "average_order_value": float(average_order_value),
            "total_refunds": float(total_refunds),
            "platform_commission": float(platform_commission),
            "customer_growth": customer_growth,
            "driver_growth": driver_growth,
            "restaurant_growth": restaurant_growth
        }

    # ======================================================
    # LIVE ORDERS DASHBOARD
    # ======================================================


    @staticmethod
    async def get_live_orders_dashboard(db):

        result = await db.execute(
            select(Order).order_by(Order.created_at.desc())
        )

        orders = result.scalars().all()

        live_orders = []

        for order in orders:

            payment = await db.scalar(
                select(Payment).where(Payment.order_id == order.id)
            )

            restaurant = await db.get(
                Restaurant,
                order.restaurant_id
            )

            delivery_agent = None

            if order.delivery_agent_id:
                delivery_agent = await db.get(
                    DeliveryAgent,
                    order.delivery_agent_id
                )

            live_orders.append({
                "order_id": order.id,
                "customer": order.customer_name,
                "restaurant": restaurant.name if restaurant else "",
                "delivery_agent": delivery_agent.name if delivery_agent else None,
                "amount": order.total,
                "payment_method": payment.payment_method if payment else "",
                "status": str(order.status),
                "created_at": order.created_at
            })

        return {
            "live_orders": live_orders
        }