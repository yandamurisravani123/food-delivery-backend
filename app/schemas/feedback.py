from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class FeedbackCreate(BaseModel):
    user_id: UUID
    order_id: int
    rating: float
    review: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "order_id": 123,
                "rating": 4.5,
                "review": "Great delivery experience!"
            }
        }
    }


class FeedbackSuccessResponse(BaseModel):
    message: str
    experience_rating: float
    reward_points_earned: int