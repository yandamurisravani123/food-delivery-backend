# app/schemas/driver.py

from pydantic import BaseModel, EmailStr, validator


from typing import Optional
class DriverRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    confirm_password: str

    vehicle_type: str
    vehicle_number: str

    driving_license_number: str
    aadhaar_number: str

    city: str
    state: str
    pincode: str

    profile_image: str | None = None   # optional

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v
    


class DriverInfoSchema(BaseModel):
    id: str
    name: str
    online: bool


class VerificationSchema(BaseModel):
    is_verified: bool
    license_status: str
    verification_status: str


class PeakBonusSchema(BaseModel):
    active: bool
    bonus_amount: float
    expires_in_minutes: int


class EarningsSchema(BaseModel):
    today: float
    goal: float
    completed_orders: int
    total_orders: int


class ActiveOrderSchema(BaseModel):
    restaurant_name: Optional[str] = None
    distance: Optional[float] = None
    status: Optional[str] = None


class ShiftSchema(BaseModel):
    available: bool
    status: Optional[str] = None


class BoostSchema(BaseModel):
    available: bool
    zone: Optional[str] = None
    percentage: int


class DriverDashboardResponse(BaseModel):
    driver: DriverInfoSchema
    verification: VerificationSchema
    peak_hour_bonus: PeakBonusSchema
    earnings: EarningsSchema
    rating: float
    acceptance_rate: float
    active_order: ActiveOrderSchema
    shift: ShiftSchema
    boost: BoostSchema