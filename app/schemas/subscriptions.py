from pydantic import BaseModel
from datetime import datetime
from typing import Optional
 
 
class SubscriptionCreate(BaseModel):
    plan_id: int
 
 
class SubscriptionUpdate(BaseModel):
    status: Optional[str] = None
 
 
class SubscriptionResponse(BaseModel):
    id: int
    selected_plan: str
    status: str
    start_date: datetime
    end_date: datetime
 
    class Config:
        from_attributes = True
 