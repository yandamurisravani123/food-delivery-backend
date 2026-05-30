from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class CODPaymentSchema(BaseModel):
    order_id: UUID
    amount: float
    payment_method: str = "COD"
    status: Optional[str] = "Pending"