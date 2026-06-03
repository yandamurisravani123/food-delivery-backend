from pydantic import BaseModel, EmailStr
from typing import Optional


class DriverBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


class DriverCreate(DriverBase):
    password: str


class DriverLogin(BaseModel):
    email: EmailStr
    password: str


class DriverOut(DriverBase):
    id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str