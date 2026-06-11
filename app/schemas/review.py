

from pydantic import BaseModel


class RestaurantReviewRequest(BaseModel):

    order_id: str

    restaurant_id: str

    user_name: str

    comment: str

    rating: float

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "order_id": "e7e1cd58-1234-4bf9-9f6b-5f7d9f0a24b1",
                "restaurant_id": "2e2f2bac-875e-4a53-867e-5c02694a0d72",
                "user_name": "Sravani",
                "comment": "Food was tasty and delivery was quick",
                "rating": 4.5
            }
        }