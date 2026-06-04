from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID


class DeliveryAgentRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., max_length=20)

    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    vehicle_type: str = Field(..., max_length=50)
    vehicle_number: str = Field(..., max_length=50)

    driving_license_number: str = Field(..., max_length=100)
    aadhaar_number: str = Field(..., max_length=20)

    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    pincode: str = Field(..., max_length=20)



class DeliveryAgentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: EmailStr
    phone: str
    vehicle_type: str
    vehicle_number: str
    driving_license_number: str
    aadhaar_number: str
    city: str
    state: str
    pincode: str
    status: str
    is_active: bool


class DeliveryAgentRegisterResponse(BaseModel):
    message: str
    delivery_agent_id: UUID
    status: str


class MessageResponse(BaseModel):
    message: str



class ShiftResponse(BaseModel):
    id: UUID
    title: str
    start_time: str
    end_time: str
    estimated_earning: float
    is_booked: bool
    demand_tag: str | None


class DashboardResponse(BaseModel):
    driver_name: str
    online: bool

    weekly_hours: float

    estimated_earnings: float

    shifts: list

    challenge: dict

    hotspot: dict




class NearbyZoneSchema(BaseModel):
    zone_name: str
    distance_miles: float
    active_orders: int
    earnings_multiplier: float
    demand_level: str

    class Config:
        from_attributes = True


class DeliveryAgentHomeSchema(BaseModel):
    id: str
    name: str
    online: bool


class DriverHomeResponse(BaseModel):
    delivery_agent: DeliveryAgentHomeSchema

    search_placeholder: str

    nearby_zones: List[NearbyZoneSchema]

    class Config:
        from_attributes = True


class BreakStartResponse(BaseModel):
    message: str
    break_minutes: int


class BreakStatusResponse(BaseModel):
    online: bool
    is_on_break: bool
    remaining_minutes: int