from pydantic import BaseModel
from typing import Optional
from datetime import datetime
 
from app.utils.enums import CampaignType
 
from uuid import UUID
class CampaignCreate(BaseModel):
    title: str
    description: Optional[str] = None
    campaign_type: CampaignType
    discount_percentage: Optional[float] = None
    target_customers: int
    start_date: datetime
    end_date: datetime
    name: str
    total_budget: float
    daily_budget: float
 
 
class CampaignUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
 
from app.utils.enums import CampaignType, CampaignStatus
 
class CampaignOut(BaseModel):
    id: UUID
    title: str
    campaign_type: CampaignType
    status: CampaignStatus
    target_customers: int
    reach_count: int
    revenue_generated: float
    clicks: int
    orders: int
 
    class Config:
        from_attributes = True
 
class DashboardSummary(BaseModel):
    total_revenue: float
    active_campaigns: int
    total_reach: int
    total_orders: int
 