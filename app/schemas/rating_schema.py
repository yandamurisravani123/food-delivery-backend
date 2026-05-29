from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RatingCreate(BaseModel):
    customer_id: int
    driver_id: int
    order_id: int
    rating: float
    feedback_tags: Optional[List[str]] = []
    review: Optional[str] = None


class RatingResponse(BaseModel):
    id: int
    customer_id: int
    driver_id: int
    order_id: int
    rating: float
    feedback_tags: Optional[str]
    review: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True