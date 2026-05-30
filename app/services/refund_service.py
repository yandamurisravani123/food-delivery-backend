from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.refund import Refund
from app.services.wallet_service import WalletService


class RefundService:

    @staticmethod
    async def initiate_refund(db: AsyncSession, data):

        refund = Refund(
            order_id=data.order_id,
            user_id=data.user_id,
            amount=data.amount,
            status="Initiated"
        )

        db.add(refund)

        await WalletService.add_money(
            db,
            data.user_id,
            data.amount
        )

        await db.commit()
        await db.refresh(refund)

        return refund

    @staticmethod
    async def get_refund(db, order_id):

        result = await db.execute(
            select(Refund).where(Refund.order_id == order_id)
        )

        return result.scalars().first()