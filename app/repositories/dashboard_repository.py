from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
<<<<<<< HEAD

from app.models.order import Order


class DashboardRepository:

=======
 
from app.models.order import Order
 
 
class DashboardRepository:
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    def get_total_orders(
        db: Session,
        restaurant_id
    ):
        return (
            db.query(Order)
            .filter(Order.restaurant_id == restaurant_id)
            .count()
        )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_orders_by_time(
        session: AsyncSession,
        restaurant_id
    ):
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        query = (
            select(
                func.extract("dow", Order.created_at).label("day"),
                func.extract("hour", Order.created_at).label("hour"),
                func.count(Order.id).label("orders")
            )
            .where(Order.restaurant_id == restaurant_id)
            .group_by("day", "hour")
        )
<<<<<<< HEAD

        result = await session.execute(query)

        return result.all()

=======
 
        result = await session.execute(query)
 
        return result.all()
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_peak_hour_orders(
        session: AsyncSession,
        restaurant_id
    ):
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        query = (
            select(
                func.extract("hour", Order.created_at).label("hour"),
                func.count(Order.id).label("orders")
            )
            .where(Order.restaurant_id == restaurant_id)
            .group_by("hour")
            .order_by(func.count(Order.id).desc())
            .limit(1)
        )
<<<<<<< HEAD

        result = await session.execute(query)

        return result.first()

    # -----------------------------
    # Dashboard APIs
    # -----------------------------

=======
 
        result = await session.execute(query)
 
        return result.first()
 
    # -----------------------------
    # Dashboard APIs
    # -----------------------------
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_growth_metrics(
        session: AsyncSession,
        restaurant_id
    ):
        return {
            "growth_index": 0,
            "target": 0,
            "monthly_growth": 0
        }
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_repeat_orders(
        session: AsyncSession,
        restaurant_id
    ):
        return {
            "retention_rate": 0,
            "monthly_growth": 0,
            "top_percentile": 0
        }
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_market_reach(
        session: AsyncSession,
        restaurant_id
    ):
        return {
            "market_share": 0,
            "growth": 0
        }
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_rating_trend(
        session: AsyncSession,
        restaurant_id
    ):
        return []
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_competitor_benchmark(
        session: AsyncSession,
        restaurant_id
    ):
        return {
            "average_prep_time": "0m",
            "accuracy": "0%",
            "customer_price_index": "N/A"
        }
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_marketing_impact(
        session: AsyncSession,
        restaurant_id
    ):
        return {
            "referral_growth": 0,
            "campaign_status": "Inactive"
        }
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_stock_efficiency(
        session: AsyncSession,
        restaurant_id
    ):
        return {
            "wastage_reduction": 0,
            "prediction_accuracy": 0
        }
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_staff_performance(
        session: AsyncSession,
        restaurant_id
    ):
        return {
            "shift_rating": 0,
            "peak_hour": "N/A"
        }
<<<<<<< HEAD
    
    

=======
   
   
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_prep_analysis(
        session: AsyncSession,
        restaurant_id
        ):
        peak_hour = await DashboardRepository.get_peak_hour_orders(
            session,
            restaurant_id
            )
        peak_hour_value = int(peak_hour.hour) if peak_hour else 12
        peak_query = (
            select(
                func.avg(Order.preparation_time)
                )
                .where(
                    Order.restaurant_id == restaurant_id,
                    func.extract("hour", Order.created_at) == peak_hour_value
                    )
                    )
        off_peak_query = (
            select(
                func.avg(Order.preparation_time)
                )
                .where(
                    Order.restaurant_id == restaurant_id,
                    func.extract("hour", Order.created_at) != peak_hour_value
                    )
                    )
        peak_result = await session.execute(peak_query)
        off_peak_result = await session.execute(off_peak_query)
        peak_avg = peak_result.scalar() or 0
        off_peak_avg = off_peak_result.scalar() or 0
        return {
            "peak_hour_prep_time": round(peak_avg, 2),
            "off_peak_prep_time": round(off_peak_avg, 2),
            "target_difference": round(
                peak_avg - off_peak_avg,
                2
                ),
                "optimization_tip":
                "Increase kitchen staff during peak hours"
                if peak_avg > off_peak_avg
                else "Preparation performance is healthy"
                }