from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class RatingCreate(BaseModel):
    customer_id: UUID
    driver_id: Optional[UUID] = None
    order_id: UUID
    rating: int
    feedback: Optional[str] = None
    tag: Optional[str] = None


class RatingResponse(BaseModel):
    id: UUID
    customer_id: UUID
    driver_id: Optional[UUID] = None
    order_id: UUID
    rating: int
    feedback: Optional[str] = None
    tag: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str