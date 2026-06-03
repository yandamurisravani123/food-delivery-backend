from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum


class PaymentMethod(str, Enum):
    COD = "COD"
    PHONEPE = "PHONEPE"
    GPAY = "GPAY"
    PAYTM = "PAYTM"
    AMAZONPAY = "AMAZONPAY"
    UPI = "UPI"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"


class PaymentRequest(BaseModel):
    order_id: UUID
    amount: float
    payment_method: PaymentMethod
    status: Optional[str] = "Pending"


class CODPaymentSchema(PaymentRequest):
    pass