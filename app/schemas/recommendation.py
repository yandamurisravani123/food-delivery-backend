from pydantic import BaseModel


class RecommendationResponse(BaseModel):

    food_name: str

    description: str

    category: str

    match_percent: int

    rating: float

    preparation_time: str

    reason: str

    tags: str