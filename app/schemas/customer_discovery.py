from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class RestaurantResponse(BaseModel):
    id: UUID
    restaurant_name: str
    cuisine_types: Optional[str]
    city: Optional[str]
    logo_url: Optional[str]

    class Config:
        from_attributes = True


class MenuSearchResponse(BaseModel):
    id: UUID
    item_name: str
    category: Optional[str]
    base_price: float
    image_url: Optional[str]

    class Config:
        from_attributes = True