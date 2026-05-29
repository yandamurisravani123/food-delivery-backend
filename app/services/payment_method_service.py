from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_method import PaymentMethod


class PaymentMethodService:

    @staticmethod
    async def create_payment_method(
        db: AsyncSession,
        data
    ):
        payment = PaymentMethod(**data.dict())

        db.add(payment)
        await db.commit()
        await db.refresh(payment)

        return payment

    @staticmethod
    async def get_payment_method(
        db: AsyncSession,
        payment_method_id: int
    ):
        result = await db.execute(
            select(PaymentMethod).where(
                PaymentMethod.id == payment_method_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_customer_payments(
        db: AsyncSession,
        customer_id: int
    ):
        result = await db.execute(
            select(PaymentMethod).where(
                PaymentMethod.customer_id == customer_id
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_all_payments(
        db: AsyncSession
    ):
        result = await db.execute(
            select(PaymentMethod)
        )
        return result.scalars().all()

    @staticmethod
    async def update_payment_method(
        db: AsyncSession,
        payment_method,
        data
    ):
        for key, value in data.dict(
            exclude_unset=True
        ).items():
            setattr(payment_method, key, value)

        await db.commit()
        await db.refresh(payment_method)

        return payment_method

    @staticmethod
    async def delete_payment_method(
        db: AsyncSession,
        payment_method
    ):
        await db.delete(payment_method)
        await db.commit()

    @staticmethod
    async def set_default(
        db: AsyncSession,
        payment_method
    ):
        result = await db.execute(
            select(PaymentMethod).where(
                PaymentMethod.customer_id
                == payment_method.customer_id
            )
        )

        methods = result.scalars().all()

        for item in methods:
            item.is_default = False

        payment_method.is_default = True

        await db.commit()

    @staticmethod
    async def activate(
        db: AsyncSession,
        payment_method
    ):
        payment_method.is_active = True
        await db.commit()

    @staticmethod
    async def deactivate(
        db: AsyncSession,
        payment_method
    ):
        payment_method.is_active = False
        await db.commit()