from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class PaymentMethodCreate(BaseModel):
    customer_id: UUID
    payment_type: str
    provider_name: str

    upi_id: Optional[str] = None

    card_holder_name: Optional[str] = None
    card_number: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None

    wallet_number: Optional[str] = None


class PaymentMethodUpdate(BaseModel):
    payment_type: Optional[str] = None
    provider_name: Optional[str] = None

    upi_id: Optional[str] = None

    card_holder_name: Optional[str] = None
    card_number: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None

    wallet_number: Optional[str] = None


class PaymentMethodResponse(BaseModel):
    id: int
    customer_id: UUID
    payment_type: str
    provider_name: str
    is_default: bool
    is_active: bool

    class Config:
        from_attributes = True