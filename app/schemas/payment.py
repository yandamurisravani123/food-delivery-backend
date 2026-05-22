from uuid import UUID

from pydantic import BaseModel


class CODPaymentSchema(BaseModel):

    order_id: UUID

    user_id: UUID

    amount: float