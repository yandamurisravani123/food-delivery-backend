from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
 
 
class OrderItemCreate(BaseModel):
    name: str
    quantity: int
    price: float
 
 
class OrderItemResponse(BaseModel):
    order_id: int
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
    cutlery_required: bool = True
 
 
class OrderResponse(BaseModel):
    order_id: int
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
    start_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None
 
    prep_time: int
    is_urgent: str
 
    delivery_address: Optional[str] = None
    courier_name: Optional[str] = None
    courier_rating: Optional[str] = None
 
    special_instructions: Optional[str] = None
    packaging_notes: Optional[str] = None
    cutlery_required: bool
 
    class Config:
        from_attributes = True
 