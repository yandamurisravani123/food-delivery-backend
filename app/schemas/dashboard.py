from typing import List
from pydantic import BaseModel


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
