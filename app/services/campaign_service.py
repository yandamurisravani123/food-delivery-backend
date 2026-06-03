from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign
from app.schemas.campaign_schema import CampaignCreate, CampaignUpdate
from app.utils.enums import CampaignStatus


class CampaignService:

    @staticmethod
    async def create_campaign(db: AsyncSession, payload: CampaignCreate, restaurant_id: UUID):
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
            end_date=payload.end_date,
        )
        db.add(campaign)
        await db.commit()
        await db.refresh(campaign)
        return campaign

    @staticmethod
    async def get_all_campaigns(db: AsyncSession):
        result = await db.execute(select(Campaign).order_by(Campaign.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def get_campaign_by_id(db: AsyncSession, campaign_id: int):
        result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_campaign(db: AsyncSession, campaign: Campaign, payload: CampaignUpdate):
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(campaign, key, value)
        await db.commit()
        await db.refresh(campaign)
        return campaign

    @staticmethod
    async def delete_campaign(db: AsyncSession, campaign: Campaign):
        await db.delete(campaign)
        await db.commit()


class DashboardService:

    @staticmethod
    async def get_summary(db: AsyncSession):
        active_campaigns = await db.scalar(
            select(func.count()).select_from(Campaign).where(Campaign.status == CampaignStatus.ACTIVE)
        )
        total_revenue = await db.scalar(select(func.sum(Campaign.revenue_generated)))
        total_reach = await db.scalar(select(func.sum(Campaign.reach_count)))
        total_orders = await db.scalar(select(func.sum(Campaign.orders)))
        return {
            "total_revenue": total_revenue or 0,
            "active_campaigns": active_campaigns or 0,
            "total_reach": total_reach or 0,
            "total_orders": total_orders or 0,
        }

    @staticmethod
    async def get_analytics(db: AsyncSession):
        impressions = await db.scalar(select(func.sum(Campaign.reach_count)))
        clicks = await db.scalar(select(func.sum(Campaign.clicks)))
        orders = await db.scalar(select(func.sum(Campaign.orders)))
        conversion_rate = (clicks / impressions) * 100 if impressions and clicks else 0
        return {
            "impressions": impressions or 0,
            "clicks": clicks or 0,
            "orders": orders or 0,
            "conversion_rate": round(conversion_rate, 2),
        }


class AnalyticsService:

    @staticmethod
    async def dashboard_summary(db):
        result = await db.execute(select(Campaign))
        campaigns = result.scalars().all()
        total_impressions = sum(c.reach_count for c in campaigns)
        total_clicks = sum(c.clicks for c in campaigns)
        total_orders = sum(c.orders for c in campaigns)
        total_revenue = sum(c.revenue_generated for c in campaigns)
        conversion_rate = (total_orders / total_clicks) * 100 if total_clicks > 0 else 0
        return {
            "impressions": total_impressions,
            "clicks": total_clicks,
            "orders": total_orders,
            "revenue": total_revenue,
            "conversion_rate": round(conversion_rate, 2),
        }


class BiddingService:

    @staticmethod
    def calculate_suggested_bid(views: int, rank: int, base: float):
        if rank > 5:
            return base * 1.5
        if views > 10000:
            return base * 1.2
        return base
