from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
 
from app.models.campaign import Campaign
from app.schemas.campaign_schema import (
    CampaignCreate,
    CampaignUpdate
)
from uuid import UUID
 
class CampaignService:
 
    @staticmethod
    async def create_campaign(
        db: AsyncSession,
        payload: CampaignCreate,
        restaurant_id: UUID
    ):
 
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
 
        db.add(campaign)
 
        await db.commit()
 
        await db.refresh(campaign)
 
        return campaign
 
    @staticmethod
    async def get_all_campaigns(db: AsyncSession):
 
        result = await db.execute(
            select(Campaign)
            .order_by(Campaign.created_at.desc())
        )
 
        return result.scalars().all()
    @staticmethod
    async def get_campaign_by_id(
        db: AsyncSession,
        campaign_id: UUID   
    ):
        result = await db.execute(
            select(Campaign).where(Campaign.id == campaign_id)
        )
        return result.scalar_one_or_none()
 
    @staticmethod
    async def update_campaign(
        db: AsyncSession,
        campaign: Campaign,
        payload: CampaignUpdate
    ):
 
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(campaign, key, value)
 
        await db.commit()
        await db.refresh(campaign)
 
        return campaign
 
    @staticmethod
    async def delete_campaign(
        db: AsyncSession,
        campaign: Campaign
    ):
 
        await db.delete(campaign)
 
        await db.commit()
        
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.utils.enums import CampaignStatus


class DashboardService:

    @staticmethod
    async def get_summary(db: AsyncSession):

        active_campaigns = await db.scalar(
            select(func.count(Campaign.id))
            .where(Campaign.status == CampaignStatus.ACTIVE)
        ) or 0

        total_revenue = await db.scalar(
            select(func.sum(Campaign.total_budget))
        ) or 0

        total_reach = await db.scalar(
            select(func.sum(Campaign.target_customers))
        ) or 0

        total_orders = await db.scalar(
            select(func.sum(Campaign.orders))
        ) or 0

        return {
            "total_revenue": float(total_revenue),
            "active_campaigns": active_campaigns,
            "total_reach": int(total_reach),
            "total_orders": int(total_orders)
        }

    @staticmethod
    async def get_analytics(db: AsyncSession):

        impressions = await db.scalar(
            select(func.sum(Campaign.reach_count))
        ) or 0

        clicks = await db.scalar(
            select(func.sum(Campaign.clicks))
        ) or 0

        orders = await db.scalar(
            select(func.sum(Campaign.orders))
        ) or 0

        conversion_rate = (
            (orders / clicks) * 100
            if clicks > 0 else 0
        )

        return {
            "impressions": int(impressions),
            "clicks": int(clicks),
            "orders": int(orders),
            "conversion_rate": round(conversion_rate, 2)
        }
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign


class AnalyticsService:

    @staticmethod
    async def dashboard_summary(db: AsyncSession):

        result = await db.execute(select(Campaign))
        campaigns = result.scalars().all()

        total_impressions = sum(getattr(c, "reach_count", 0) or 0 for c in campaigns)
        total_clicks = sum(getattr(c, "clicks", 0) or 0 for c in campaigns)
        total_orders = sum(getattr(c, "orders", 0) or 0 for c in campaigns)
        total_revenue = sum(getattr(c, "total_budget", 0) or 0 for c in campaigns)

        conversion_rate = (
            (total_orders / total_clicks) * 100
            if total_clicks > 0 else 0
        )

        return {
            "impressions": total_impressions,
            "clicks": total_clicks,
            "orders": total_orders,
            "revenue": total_revenue,
            "conversion_rate": round(conversion_rate, 2)
        }
class BiddingService:

    @staticmethod
    def calculate_suggested_bid(views: int, rank: int, base: float):

        if rank > 5:
            return base * 1.5

        if views > 10000:
            return base * 1.2

        return base