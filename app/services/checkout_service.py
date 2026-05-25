from app.repositories.checkout_repository import CheckoutRepository


class CheckoutService:

    @staticmethod
    async def create_checkout(db, payload):

        total = payload.subtotal + payload.delivery_fee

        data = {
            "user_id": payload.user_id,
            "address": payload.address,
            "delivery_date": payload.delivery_date,
            "delivery_time": payload.delivery_time,
            "payment_method": payload.payment_method,
            "subtotal": payload.subtotal,
            "delivery_fee": payload.delivery_fee,
            "total": total,
            "is_paid": False
        }

        checkout = await CheckoutRepository.create_checkout(
            db,
            data
        )

        return {
            "id": str(checkout.id),
            "message": "Order Scheduled Successfully"
        }