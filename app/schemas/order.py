from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: UUID
    food_name: str
    cuisine: str
    order_time: datetime


class OrderResponse(BaseModel):
    id: int
    user_id: UUID
    food_name: str
    cuisine: str
    order_time: datetime

    class Config:
        from_attributes = True