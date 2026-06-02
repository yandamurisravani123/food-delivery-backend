from pydantic import BaseModel
from uuid import UUID
 
 
class RefundCreate(BaseModel):
    order_id: UUID
    user_id: UUID
    amount: float
 
 
class RefundStatusUpdate(BaseModel):
    status: str
 