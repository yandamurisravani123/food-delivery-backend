from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class AddMoneySchema(BaseModel):
    user_id: UUID
    amount: float


class TransferMoneySchema(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    amount: float


class WalletResponse(BaseModel):
    user_id: UUID
    balance: float

    class Config:
        from_attributes = True