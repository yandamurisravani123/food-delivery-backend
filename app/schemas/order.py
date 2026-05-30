<<<<<<< HEAD
from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class OrderItemCreate(BaseModel):
    name: str
    quantity: int
    price: float


class OrderItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True
        
class OrderCreate(BaseModel):
    user_id: UUID
    restaurant_id: UUID

    items: List[OrderItemCreate]  

    delivery_address: Optional[str] = None
    special_instructions: Optional[str] = None
    cutlery_required: Optional[bool] = True

class OrderResponse(BaseModel):
    id: int
    user_id: UUID
    restaurant_id: UUID

    items: List[OrderItemResponse]   

    subtotal: float
    delivery_fee: float
    tax_percent: float
    total: float

    status: str

    order_time: datetime
    created_at: datetime
    start_time: Optional[datetime]
    completed_at: Optional[datetime]

    prep_time: int
    is_urgent: str

    delivery_address: Optional[str]
    courier_name: Optional[str]
    courier_rating: Optional[str]

    special_instructions: Optional[str]
    packaging_notes: Optional[str]
    cutlery_required: bool

    class Config:
        from_attributes = True
=======
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=True)

    total_amount = Column(Float, default=0)
    group_size = Column(Integer, default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
>>>>>>> smart-bidding-feature
