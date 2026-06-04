

from uuid import UUID
from pydantic import BaseModel


class RestaurantReviewRequest(BaseModel):

    order_id: UUID

    restaurant_id: UUID

    user_name: str

    comment: str

    rating: float

    class Config:
        from_attributes = True