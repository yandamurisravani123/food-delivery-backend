from pydantic import BaseModel
from typing import Literal, Optional
from uuid import UUID


class PaymentRequest(BaseModel):
    order_id: UUID
    amount: float
    payment_method: Literal["COD"] = "COD"
    status: Optional[str] = "Pending"


class CODPaymentSchema(PaymentRequest):
    pass
 