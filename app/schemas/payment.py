from pydantic import BaseModel
from typing import Literal, Optional


class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    payment_method: Literal["COD"] = "COD"
    status: Optional[str] = "Pending"


class PaymentResponse(BaseModel):
    message: str
    order_id: int
    amount: float
    payment_method: str
    status: str


class CODPaymentSchema(PaymentRequest):
    pass