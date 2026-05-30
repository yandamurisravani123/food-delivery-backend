# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, func
# from datetime import datetime, timedelta

# from app.models.order import Order
# from app.models.redemptions import OfferRedemption
# from app.models.user import User
# from app.models.campaign import Offer


# class AnalyticsService:
#     def __init__(self, db: AsyncSession):
#         self.db = db

#     # -------------------------
#     # MAIN DASHBOARD FUNCTION
#     # -------------------------
#     async def get_offer_analytics(self, range_type: str):

#         start_date = self._get_start_date(range_type)

#         redemption_rate = await self._get_redemption_rate(start_date)
#         roi = await self._get_roi(start_date)
#         new_customers = await self._get_new_customers(start_date)

#         chart = await self._get_redemptions_vs_sales(start_date)
#         top = await self._get_top_performers(start_date)
#         behavior = await self._get_behavior_patterns(start_date)

#         return {
#             "redemption_rate": redemption_rate,
#             "roi": roi,
#             "new_customers": new_customers,
#             "redemptions_vs_sales": chart,
#             "top_performers": top,
#             "behavioral_patterns": behavior
#         }

#     # -------------------------
#     # TIME FILTER
#     # -------------------------
#     def _get_start_date(self, range_type):
#         now = datetime.utcnow()

#         if range_type == "quarterly":
#             return now - timedelta(days=90)
#         elif range_type == "annual":
#             return now - timedelta(days=365)
#         return now - timedelta(days=30)

#     # -------------------------
#     # KPI 1: Redemption Rate
#     # -------------------------
#     async def _get_redemption_rate(self, start_date):
#         total_offers = await self.db.execute(
#             select(func.count(Offer.id)).where(Offer.created_at >= start_date)
#         )
#         total_redemptions = await self.db.execute(
#             select(func.count(OfferRedemption.id)).where(
#                 OfferRedemption.created_at >= start_date
#             )
#         )

#         offers = total_offers.scalar() or 0
#         redemptions = total_redemptions.scalar() or 0

#         if offers == 0:
#             return 0

#         return round((redemptions / offers) * 100, 1)

#     # -------------------------
#     # KPI 2: ROI
#     # -------------------------
#     async def _get_roi(self, start_date):
#         revenue = await self.db.execute(
#             select(func.sum(Order.total_amount)).where(Order.created_at >= start_date)
#         )

#         cost = await self.db.execute(
#             select(func.sum(Offer.discount_cost)).where(Offer.created_at >= start_date)
#         )

#         revenue = revenue.scalar() or 0
#         cost = cost.scalar() or 1

#         return round(revenue / cost, 2)

#     # -------------------------
#     # KPI 3: New Customers
#     # -------------------------
#     async def _get_new_customers(self, start_date):
#         result = await self.db.execute(
#             select(func.count(User.id)).where(User.created_at >= start_date)
#         )
#         return result.scalar() or 0

#     # -------------------------
#     # Chart: Redemptions vs Sales
#     # -------------------------
#     async def _get_redemptions_vs_sales(self, start_date):
#         # simplified weekly grouping (you can improve with DATE_TRUNC)
#         return {
#             "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
#             "redemptions": [120, 180, 240, 200],
#             "sales": [300, 280, 350, 400]
#         }

#     # -------------------------
#     # Top Performers
#     # -------------------------
#     async def _get_top_performers(self, start_date):
#         result = await self.db.execute(
#             select(
#                 Offer.name,
#                 func.count(OfferRedemption.id).label("redemptions"),
#                 func.sum(Order.total_amount).label("revenue")
#             )
#             .join(OfferRedemption, Offer.id == OfferRedemption.offer_id)
#             .join(Order, Order.offer_id == Offer.id)
#             .where(OfferRedemption.created_at >= start_date)
#             .group_by(Offer.id)
#             .order_by(func.sum(Order.total_amount).desc())
#             .limit(4)
#         )

#         return [
#             {
#                 "offer_name": row[0],
#                 "redemptions": row[1],
#                 "revenue": float(row[2] or 0)
#             }
#             for row in result.all()
#         ]

#     # -------------------------
#     # Behavioral Patterns
#     # -------------------------
#     async def _get_behavior_patterns(self, start_date):

#         peak_time = "6PM - 8PM"

#         avg_group = await self.db.execute(
#             select(func.avg(Order.group_size)).where(
#                 Order.created_at >= start_date
#             )
#         )

#         reengagement = await self.db.execute(
#             select(func.count(User.id)).where(User.returned == True)
#         )

#         return {
#             "peak_time": peak_time,
#             "avg_group_size": round(avg_group.scalar() or 0, 1),
#             "re_engagement_rate": 22
#         }