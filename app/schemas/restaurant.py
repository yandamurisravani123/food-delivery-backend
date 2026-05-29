from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID


class RestaurantRegisterRequest(BaseModel):
    restaurant_name: str = Field(..., min_length=2, max_length=150)
    owner_name: str = Field(..., min_length=2, max_length=100)
    owner_email: EmailStr
    owner_phone: str = Field(..., max_length=20)
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    restaurant_phone: str = Field(..., max_length=20)
    cuisine_types: Optional[str] = Field(default=None, max_length=255)

    address_line1: str = Field(..., max_length=255)
    address_line2: Optional[str] = Field(default=None, max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    pincode: str = Field(..., max_length=20)

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    opening_time: Optional[str] = Field(default=None, max_length=20)
    closing_time: Optional[str] = Field(default=None, max_length=20)

    gst_number: Optional[str] = Field(default=None, max_length=50)
    fssai_number: Optional[str] = Field(default=None, max_length=50)
    logo_url: Optional[str] = Field(default=None, max_length=255)


class RestaurantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    restaurant_name: str
    owner_name: str
    owner_email: EmailStr
    owner_phone: str
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
    gst_number: Optional[str] = None
    fssai_number: Optional[str] = None
    logo_url: Optional[str] = None
    status: str
    is_active: bool


class RestaurantApprovalResponse(BaseModel):
    message: str



class RestaurantRegisterResponse(BaseModel):
    message: str
    restaurant_id: UUID
    status: str
