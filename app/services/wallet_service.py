from decimal import Decimal
 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
 
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction
 
 
class WalletService:
 
    @staticmethod
    async def get_wallet(db: AsyncSession, user_id):
 
        result = await db.execute(
            select(Wallet).where(Wallet.user_id == user_id)
        )
 
        return result.scalars().first()
 
    @staticmethod
    async def add_money(db: AsyncSession, user_id, amount):
 
        amount = Decimal(str(amount))
 
        wallet = await WalletService.get_wallet(db, user_id)
 
        if not wallet:
            wallet = Wallet(
                user_id=user_id,
                balance=Decimal("0.00")
            )
 
            db.add(wallet)
 
        wallet.balance += amount
 
        transaction = WalletTransaction(
            user_id=user_id,
            transaction_type="CREDIT",
            amount=float(amount),
            description="Added to Wallet"
        )
 
        db.add(transaction)
 
        await db.commit()
        await db.refresh(wallet)
 
        return wallet
 
    @staticmethod
    async def transfer_money(
        db: AsyncSession,
        sender_id,
        receiver_id,
        amount
    ):
 
        amount = Decimal(str(amount))
 
        sender = await WalletService.get_wallet(db, sender_id)
        receiver = await WalletService.get_wallet(db, receiver_id)
 
        if not sender:
            raise Exception("Sender wallet not found")
 
        if sender.balance < amount:
            raise Exception("Insufficient balance")
 
        sender.balance -= amount
 
        if not receiver:
            receiver = Wallet(
                user_id=receiver_id,
                balance=Decimal("0.00")
            )
 
            db.add(receiver)
 
        receiver.balance += amount
 
        db.add(
            WalletTransaction(
                user_id=sender_id,
                transaction_type="DEBIT",
                amount=float(amount),
                description="Transfer Sent"
            )
        )
 
        db.add(
            WalletTransaction(
                user_id=receiver_id,
                transaction_type="CREDIT",
                amount=float(amount),
                description="Transfer Received"
            )
        )
 
        await db.commit()
 
        return {
            "message": "Transfer successful"
        }
 