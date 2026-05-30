import uuid

from app.models.payment import Payment


class PaymentService:

    @staticmethod
    async def make_payment(db, payload):

        payment_method = payload.payment_method.upper()

        allowed_methods = [
            "COD",
            "GPAY",
            "PHONEPE",
            "AMAZON_PAY",
            "PAYTM",
            "CREDIT_CARD"
        ]

        if payment_method not in allowed_methods:

            return {
                "success": False,
                "message": "Invalid payment method"
            }

        payment_status = (
            "PENDING"
            if payment_method == "COD"
            else "SUCCESS"
        )

        payment = Payment(
            order_id=payload.order_id,
            user_id=payload.user_id,
            payment_method=payment_method,
            payment_status=payment_status,
            amount=float(payload.amount),
            transaction_id=str(uuid.uuid4())
        )

        db.add(payment)

        await db.commit()

        await db.refresh(payment)

        return {
            "success": True,
            "message": f"{payment_method} payment successful",
            "payment": payment
        }