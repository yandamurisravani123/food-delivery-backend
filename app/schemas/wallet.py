from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
 
 
class AddMoneySchema(BaseModel):
    user_id: UUID
    amount: Decimal
 
 
class TransferMoneySchema(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    amount: Decimal
 
 
class WalletResponse(BaseModel):
    user_id: UUID
    balance: float
 
    class Config:
        from_attributes = True
 