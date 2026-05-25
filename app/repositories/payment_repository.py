from sqlalchemy.ext.asyncio import AsyncSession
from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    async def create_payment(
        db: AsyncSession,
        data: dict
    ):

        payment = Payment(**data)

        db.add(payment)

        await db.commit()

        await db.refresh(payment)

        return payment