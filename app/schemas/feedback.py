from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class FeedbackCreate(BaseModel):
    user_id: UUID
    order_id: int
    rating: float
    review: Optional[str] = None


class FeedbackSuccessResponse(BaseModel):
    message: str
    experience_rating: float
    reward_points_earned: int