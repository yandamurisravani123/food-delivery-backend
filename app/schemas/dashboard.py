from pydantic import BaseModel
from typing import List
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class HeatmapCell(BaseModel):
    day: str
    hour: str
    orders: int
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class PeakHourCard(BaseModel):
    title: str
    peak_time: str
    revenue_percentage: float
<<<<<<< HEAD


class StaffSuggestion(BaseModel):
    suggestions: List[str]


=======
 
 
class StaffSuggestion(BaseModel):
    suggestions: List[str]
 
 
>>>>>>> 6da5f03 (testing)
class PreparationAnalysis(BaseModel):
    peak_hour_prep_time: int
    off_peak_prep_time: int
    target_difference: int
    optimization_tip: str
<<<<<<< HEAD


=======
 
 
>>>>>>> 6da5f03 (testing)
class DashboardSummaryResponse(BaseModel):
    heatmap: List[HeatmapCell]
    peak_card: PeakHourCard
    staff_planning: StaffSuggestion
    prep_analysis: PreparationAnalysis