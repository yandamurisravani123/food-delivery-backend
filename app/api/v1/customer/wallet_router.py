from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.config.database import get_db
 
from app.schemas.wallet import (
    AddMoneySchema,
    TransferMoneySchema
)
 
from app.services.wallet_service import WalletService
 
router = APIRouter(prefix="/wallet", tags=["Wallet"])
 
 
@router.get("/{user_id}")
async def get_wallet(user_id, db: AsyncSession = Depends(get_db)):
 
    return await WalletService.get_wallet(db, user_id)
 
 
@router.post("/add-money")
async def add_money(
    payload: AddMoneySchema,
    db: AsyncSession = Depends(get_db)
):
 
    return await WalletService.add_money(
        db,
        payload.user_id,
        payload.amount
    )
 
 
@router.post("/transfer")
async def transfer_money(
    payload: TransferMoneySchema,
    db: AsyncSession = Depends(get_db)
):
 
    return await WalletService.transfer_money(
        db,
        payload.sender_id,
        payload.receiver_id,
        payload.amount
    )
 