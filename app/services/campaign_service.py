from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
from app.models.campaign import Campaign
from app.schemas.campaign_schema import (
    CampaignCreate,
    CampaignUpdate
)
from uuid import UUID
<<<<<<< HEAD

class CampaignService:

=======
 
class CampaignService:
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def create_campaign(
        db: AsyncSession,
        payload: CampaignCreate,
        restaurant_id: UUID
    ):
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        campaign = Campaign(
            restaurant_id=restaurant_id,
            title=payload.title,
            description=payload.description,
            campaign_type=payload.campaign_type,
            discount_percentage=payload.discount_percentage,
            target_customers=payload.target_customers,
            daily_budget=payload.daily_budget,
            total_budget=payload.total_budget,
            start_date=payload.start_date,
            end_date=payload.end_date
        )
<<<<<<< HEAD

        db.add(campaign)

        await db.commit()

        await db.refresh(campaign)

        return campaign

    @staticmethod
    async def get_all_campaigns(db: AsyncSession):

=======
 
        db.add(campaign)
 
        await db.commit()
 
        await db.refresh(campaign)
 
        return campaign
 
    @staticmethod
    async def get_all_campaigns(db: AsyncSession):
 
>>>>>>> 6da5f03 (testing)
        result = await db.execute(
            select(Campaign)
            .order_by(Campaign.created_at.desc())
        )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        return result.scalars().all()
    @staticmethod
    async def get_campaign_by_id(
        db: AsyncSession,
        campaign_id: int
    ):
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        result = await db.execute(
            select(Campaign)
            .where(Campaign.id == campaign_id)
        )
<<<<<<< HEAD

        return result.scalar_one_or_none()

=======
 
        return result.scalar_one_or_none()
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def update_campaign(
        db: AsyncSession,
        campaign: Campaign,
        payload: CampaignUpdate
    ):
<<<<<<< HEAD

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(campaign, key, value)

        await db.commit()
        await db.refresh(campaign)

        return campaign

=======
 
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(campaign, key, value)
 
        await db.commit()
        await db.refresh(campaign)
 
        return campaign
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def delete_campaign(
        db: AsyncSession,
        campaign: Campaign
    ):
<<<<<<< HEAD

        await db.delete(campaign)

        await db.commit()

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.utils.enums import CampaignStatus


class DashboardService:

    @staticmethod
    async def get_summary(db: AsyncSession):

=======
 
        await db.delete(campaign)
 
        await db.commit()
 
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.models.campaign import Campaign
from app.utils.enums import CampaignStatus
 
 
class DashboardService:
 
    @staticmethod
    async def get_summary(db: AsyncSession):
 
>>>>>>> 6da5f03 (testing)
        active_campaigns = await db.scalar(
            select(func.count())
            .select_from(Campaign)
            .where(Campaign.status == CampaignStatus.ACTIVE)
        )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        total_revenue = await db.scalar(
            select(func.sum(Campaign.revenue_generated))
        )
        total_reach = await db.scalar(
            select(func.sum(Campaign.reach_count))
        )
<<<<<<< HEAD

        total_orders = await db.scalar(
            select(func.sum(Campaign.orders))
        )

=======
 
        total_orders = await db.scalar(
            select(func.sum(Campaign.orders))
        )
 
>>>>>>> 6da5f03 (testing)
        return {
            "total_revenue": total_revenue or 0,
            "active_campaigns": active_campaigns or 0,
            "total_reach": total_reach or 0,
            "total_orders": total_orders or 0
        }
<<<<<<< HEAD
    

    @staticmethod
    async def get_analytics(db: AsyncSession):

        impressions = await db.scalar(
            select(func.sum(Campaign.reach_count))
        )

        clicks = await db.scalar(
            select(func.sum(Campaign.clicks))
        )

        orders = await db.scalar(
            select(func.sum(Campaign.orders))
        )

        conversion_rate = 0

        if impressions and clicks:
            conversion_rate = (clicks / impressions) * 100

=======
   
 
    @staticmethod
    async def get_analytics(db: AsyncSession):
 
        impressions = await db.scalar(
            select(func.sum(Campaign.reach_count))
        )
 
        clicks = await db.scalar(
            select(func.sum(Campaign.clicks))
        )
 
        orders = await db.scalar(
            select(func.sum(Campaign.orders))
        )
 
        conversion_rate = 0
 
        if impressions and clicks:
            conversion_rate = (clicks / impressions) * 100
 
>>>>>>> 6da5f03 (testing)
        return {
            "impressions": impressions or 0,
            "clicks": clicks or 0,
            "orders": orders or 0,
            "conversion_rate": round(conversion_rate, 2)
        }
<<<<<<< HEAD
    
from sqlalchemy import select
from app.models.campaign import Campaign


class AnalyticsService:

    @staticmethod
    async def dashboard_summary(db):

        result = await db.execute(
            select(Campaign)
        )

        campaigns = result.scalars().all()

        total_impressions = sum(c.impressions for c in campaigns)

        total_clicks = sum(c.clicks for c in campaigns)

        total_orders = sum(c.orders for c in campaigns)

        total_revenue = sum(c.revenue for c in campaigns)

        conversion_rate = 0

=======
   
from sqlalchemy import select
from app.models.campaign import Campaign
 
 
class AnalyticsService:
 
    @staticmethod
    async def dashboard_summary(db):
 
        result = await db.execute(
            select(Campaign)
        )
 
        campaigns = result.scalars().all()
 
        total_impressions = sum(c.impressions for c in campaigns)
 
        total_clicks = sum(c.clicks for c in campaigns)
 
        total_orders = sum(c.orders for c in campaigns)
 
        total_revenue = sum(c.revenue for c in campaigns)
 
        conversion_rate = 0
 
>>>>>>> 6da5f03 (testing)
        if total_clicks > 0:
            conversion_rate = (
                total_orders / total_clicks
            ) * 100
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        return {
            "impressions": total_impressions,
            "clicks": total_clicks,
            "orders": total_orders,
            "revenue": total_revenue,
            "conversion_rate": round(conversion_rate, 2)
        }
<<<<<<< HEAD
    


class BiddingService:

=======
   
 
 
class BiddingService:
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    def calculate_suggested_bid(views: int, rank: int, base: float):
        if rank > 5:
            return base * 1.5
        if views > 10000:
            return base * 1.2
<<<<<<< HEAD
        return base
=======
        return base
 
>>>>>>> 6da5f03 (testing)
