from typing import Optional
from pydantic import BaseModel


class RestaurantOnboardingRequest(BaseModel):

    restaurant_name: str

    cuisine_types: str

    opening_time: str

    closing_time: str

    address_line1: str

    city: str

    state: str

    pincode: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    logo_url: Optional[str] = None

    is_draft: bool = True