from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PlanBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    duration_days: int
    free_trial_days: int = 0
    is_popular: bool = False
    is_featured: bool = False
    is_active: bool = True
    badge_text: Optional[str] = None
    button_text: Optional[str] = None
    theme_color: Optional[str] = None
    icon_url: Optional[str] = None
    display_order: int = 0


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    free_trial_days: Optional[int] = None
    is_popular: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    badge_text: Optional[str] = None
    button_text: Optional[str] = None
    theme_color: Optional[str] = None
    icon_url: Optional[str] = None
    display_order: Optional[int] = None


class PlanResponse(PlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  