import uuid

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config.database import AsyncSessionLocal
from app.schemas.payment import PaymentRequest

class PaymentService:

    @staticmethod
    async def create_payment(payload: PaymentRequest):

        payment_method = payload.payment_method.upper()

        if payment_method not in ["CASH", "UPI", "CARD"]:
            return {
                "success": False,
                "message": "Invalid payment method"
            }

        return {
            "success": True,
            "message": "Payment successful"
        }