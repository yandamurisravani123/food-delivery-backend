from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class PaymentSchema(BaseModel):

    order_id: int

    user_id: UUID

    amount: Decimal

    payment_method: str