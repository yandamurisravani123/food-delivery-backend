from pydantic import BaseModel
from typing import List, Optional
 
 
class GrowthMetric(BaseModel):
    title: str
    value: str
    change: str
    target: Optional[str] = None
    current: Optional[str] = None
 
 
class GrowthTip(BaseModel):
    title: str
    description: str
    action: str
 
 
class CompetitorBenchmark(BaseModel):
    avg_prep_time: str
    order_accuracy: str
    customer_price_index: str
 
 
class InsightCard(BaseModel):
    title: str
    description: str
    action: str
 
 
class RestaurantDashboardResponse(BaseModel):
    growth_index: GrowthMetric
    repeat_order_rate: GrowthMetric
    market_share: GrowthMetric
    merchant_rating: dict
 
    growth_tips: List[GrowthTip]
 
    competitor_benchmark: CompetitorBenchmark
 
    marketing_insight: InsightCard
    stock_efficiency: InsightCard
    staff_performance: InsightCard