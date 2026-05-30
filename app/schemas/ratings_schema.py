from pydantic import BaseModel
from typing import Optional


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
    feedback: Optional[str]
    tag: Optional[str]

    class Config:
        from_attributes = True