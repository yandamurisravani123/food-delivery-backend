from pydantic import BaseModel
from typing import List


class HeatmapPoint(BaseModel):
    latitude: float
    longitude: float
    orders: int


class OrderHeatmapResponse(BaseModel):
    heatmap: List[HeatmapPoint]