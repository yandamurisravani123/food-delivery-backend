from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RatingCreate(BaseModel):
    customer_id: int
    driver_id: int
    order_id: int
    rating: int
    feedback: Optional[str] = None
    tag: Optional[str] = None


class RatingResponse(BaseModel):
    id: int
    customer_id: int
    driver_id: int
    order_id: int
    rating: int
    feedback: Optional[str] = None
    tag: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str