from pydantic import BaseModel
from typing import List


class TransferItem(BaseModel):

    transfer_reference: str

    amount: float

    transfer_status: str

    transfer_date: str

    transfer_time: str

    class Config:

        from_attributes = True


class ReceivingAccount(BaseModel):

    bank_name: str

    account_number: str

    routing_number: str

    account_type: str


class BankTransferResponse(BaseModel):

    mtd_settlement_amount: float

    growth_percentage: float

    receiving_account: ReceivingAccount

    recent_transfers: List[TransferItem]