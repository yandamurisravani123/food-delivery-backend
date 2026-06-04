from pydantic import BaseModel

from typing import Optional


class SearchResponse(BaseModel):

    restaurant_name: str

    cuisine_types: Optional[str]

    logo_url: Optional[str]

    rating: float

    class Config:

        from_attributes = True