import uuid

from app.schemas.payment import PaymentRequest


class PaymentService:

    @staticmethod
    def create_payment(payment: PaymentRequest):
        return {
            "payment_id": str(uuid.uuid4()),
            "order_id": str(payment.order_id),
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status or "Pending",
            "message": "Payment processed successfully",
        }
