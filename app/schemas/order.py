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