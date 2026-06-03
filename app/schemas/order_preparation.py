from pydantic import BaseModel
from typing import List
from datetime import datetime


class PreparationStepSchema(BaseModel):
    title: str
    status: str
    sequence: int

    class Config:
        from_attributes = True


class OrderPreparationResponse(BaseModel):
    order_id: int
    current_stage: str
    progress_percent: int
    estimated_ready_time: datetime | None
    chef_note: str | None
    steps: List[PreparationStepSchema]