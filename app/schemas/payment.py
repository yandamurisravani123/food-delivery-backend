from pydantic import BaseModel
from typing import Literal
from uuid import UUID



class PaymentRequest(BaseModel):
    user_id: UUID
    order_id: int
    amount: float
    payment_method: Literal[
        "cash",
        "card",
        "upi",
        "phonepe",
        "gpay"
    ]

class PaymentResponse(BaseModel):

    success: bool
    id: int
    user_id: UUID
    order_id: int
    amount: float

    payment_method: str
    payment_status: str
    transaction_id: str