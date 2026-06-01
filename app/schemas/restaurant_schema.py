from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr
)

from typing import Optional


#

class RestaurantRegisterRequest(BaseModel):

    restaurant_name: str

    owner_name: str

    owner_email: EmailStr

    owner_phone: str

    password: str

    confirm_password: str

    restaurant_phone: str

    cuisine_types: Optional[str] = None

    address_line1: str

    address_line2: Optional[str] = None

    city: str

    state: str

    pincode: str

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    opening_time: Optional[str] = None

    closing_time: Optional[str] = None

    delivery_time: Optional[str] = None

    gst_number: Optional[str] = None

    fssai_number: Optional[str] = None

    logo_url: Optional[str] = None

    banner_image: Optional[str] = None



class RestaurantResponse(BaseModel):

    id: UUID

    restaurant_name: str

    owner_name: str

    owner_email: EmailStr

    restaurant_phone: str

    cuisine_types: Optional[str]

    rating: float

    delivery_time: Optional[str]

    city: str

    state: str

    logo_url: Optional[str]

    banner_image: Optional[str]

    is_active: bool

    status: str

    class Config:

        from_attributes = True