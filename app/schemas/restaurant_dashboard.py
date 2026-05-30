from pydantic import BaseModel
from typing import List, Optional
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class GrowthMetric(BaseModel):
    title: str
    value: str
    change: str
    target: Optional[str] = None
    current: Optional[str] = None
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class GrowthTip(BaseModel):
    title: str
    description: str
    action: str
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class CompetitorBenchmark(BaseModel):
    avg_prep_time: str
    order_accuracy: str
    customer_price_index: str
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class InsightCard(BaseModel):
    title: str
    description: str
    action: str
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class RestaurantDashboardResponse(BaseModel):
    growth_index: GrowthMetric
    repeat_order_rate: GrowthMetric
    market_share: GrowthMetric
    merchant_rating: dict
<<<<<<< HEAD

    growth_tips: List[GrowthTip]

    competitor_benchmark: CompetitorBenchmark

=======
 
    growth_tips: List[GrowthTip]
 
    competitor_benchmark: CompetitorBenchmark
 
>>>>>>> 6da5f03 (testing)
    marketing_insight: InsightCard
    stock_efficiency: InsightCard
    staff_performance: InsightCard