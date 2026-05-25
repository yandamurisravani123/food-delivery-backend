from typing import Optional
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