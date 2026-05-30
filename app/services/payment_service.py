import uuid

from app.repositories.payment_repository import (
    PaymentRepository
)

from app.config.database import AsyncSessionLocal
from app.schemas.payment import PaymentRequest

class PaymentService:

    @staticmethod
    async def cash_on_delivery(
        db: AsyncSession,
        payload
    ):

        payment_data = {

            "order_id": payload.order_id,

            "user_id": payload.user_id,

            "payment_method": "COD",

            "payment_status": "Pending",

            "amount": payload.amount
        }

        payment = await PaymentRepository.create_payment(
            db,
            payment_data
        )

        return {

            "message": "Cash On Delivery Order Placed Successfully",

            "payment": payment
        }