from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class PaymentMethod(str, Enum):
    COD = "COD"
    UPI = "UPI"
    CARD = "CARD"
    WALLET = "WALLET"


class SelectPaymentRequest(BaseModel):
    user_id: UUID
    order_id: int
    payment_method: PaymentMethod


class UpdatePaymentRequest(BaseModel):
    payment_method: PaymentMethod