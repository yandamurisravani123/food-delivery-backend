from datetime import datetime

from pydantic import BaseModel
from typing import List
 
 
class HeatmapCell(BaseModel):
    day: str
    hour: str
    orders: int
 
 
class PeakHourCard(BaseModel):
    title: str
    peak_time: str
    revenue_percentage: float
 
 
class StaffSuggestion(BaseModel):
    suggestions: List[str]
 
 
class PreparationAnalysis(BaseModel):
    peak_hour_prep_time: int
    off_peak_prep_time: int
    target_difference: int
    optimization_tip: str
 
 
class DashboardSummaryResponse(BaseModel):
    heatmap: List[HeatmapCell]
    peak_card: PeakHourCard
    staff_planning: StaffSuggestion
    prep_analysis: PreparationAnalysis

class OperationsDashboardResponse(BaseModel):
    total_orders: int
    pending_orders: int
    accepted_orders: int
    preparing_orders: int
    out_for_delivery: int
    completed_orders: int
    cancelled_orders: int
    total_customers: int
    total_delivery_agents: int
    active_delivery_agents: int
    offline_delivery_agents: int
    total_restaurants: int

class BusinessKPIDashboardResponse(BaseModel):
    total_revenue: float
    today_revenue: float
    monthly_revenue: float
    average_order_value: float
    total_refunds: float
    platform_commission: float
    customer_growth: float
    driver_growth: float
    restaurant_growth: float

class LiveOrder(BaseModel):
    order_id: int
    customer: str
    restaurant: str
    driver: str | None
    amount: float
    payment_method: str
    status: str
    created_at: datetime


class LiveOrdersDashboardResponse(BaseModel):
    live_orders: list[LiveOrder]