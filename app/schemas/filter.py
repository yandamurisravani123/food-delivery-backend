from pydantic import BaseModel

from typing import Optional


class FilterResponse(BaseModel):

    restaurant_name: str

    cuisine_types: Optional[str]

    rating: float

    delivery_time: Optional[str]

    class Config:

        from_attributes = True