from pydantic import BaseModel


class ReviewResponse(BaseModel):

    id: int
    user_name: str
    comment: str
    rating: float

    class Config:
        from_attributes = True