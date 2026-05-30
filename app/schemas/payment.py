from pydantic import BaseModel
from typing import Literal
from uuid import UUID
from typing import Optional


class CODPaymentSchema(BaseModel):
    order_id: UUID
    amount: float
    payment_method: str = "COD"
    status: Optional[str] = "Pending"