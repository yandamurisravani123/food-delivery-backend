

from pydantic import BaseModel


class RestaurantReviewRequest(BaseModel):

    order_id: str

    restaurant_id: str

    user_name: str

    comment: str

    rating: float

    class Config:
        from_attributes = True