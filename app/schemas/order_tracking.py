# app/schemas/order_tracking.py

from pydantic import BaseModel
from uuid import UUID


class UpdateLocationSchema(BaseModel):
    latitude: float
    longitude: float


class OrderTrackingResponse(BaseModel):
    order_id: UUID
    status: str
    estimated_time: int
    latitude: float | None
    longitude: float | None

    class Config:
        from_attributes = True