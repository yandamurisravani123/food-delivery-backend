from pydantic import BaseModel
from typing import List


class TopSellingItemResponse(BaseModel):
    item_id: int
    item_name: str
    image_url: str
    sold_units: int
    revenue: float
    market_share: float
    category: str


class CategoryInsight(BaseModel):
    category: str
    percentage: float


class RankingItem(BaseModel):
    rank: int
    item_name: str
    image_url: str
    category: str
    sold_units: int


class DashboardAnalyticsResponse(BaseModel):
    best_seller: TopSellingItemResponse
    category_insights: List[CategoryInsight]
    rankings: List[RankingItem]