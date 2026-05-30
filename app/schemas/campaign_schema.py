from pydantic import BaseModel
from typing import Optional
from datetime import datetime
<<<<<<< HEAD

from app.utils.enums import CampaignType

=======
 
from app.utils.enums import CampaignType
 
>>>>>>> 6da5f03 (testing)
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
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class CampaignUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
<<<<<<< HEAD

from app.utils.enums import CampaignType, CampaignStatus

=======
 
from app.utils.enums import CampaignType, CampaignStatus
 
>>>>>>> 6da5f03 (testing)
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
<<<<<<< HEAD

    class Config:
        from_attributes = True

=======
 
    class Config:
        from_attributes = True
 
>>>>>>> 6da5f03 (testing)
class DashboardSummary(BaseModel):
    total_revenue: float
    active_campaigns: int
    total_reach: int
<<<<<<< HEAD
    total_orders: int
=======
    total_orders: int
 
>>>>>>> 6da5f03 (testing)
