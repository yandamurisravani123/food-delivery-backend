from fastapi import HTTPException
from sqlalchemy import select
import traceback

from app.models.order import Order
from app.models.payment import Payment


class PaymentService:

    @staticmethod
    async def select_payment_method(
        db,
        payment_data
    ):
        try:

            print("Incoming data:", payment_data)

            result = await db.execute(
                select(Order).where(
                    Order.id == payment_data.order_id
                )
            )

            order = result.scalar_one_or_none()

            print("Order found:", order)

            if not order:
                raise HTTPException(
                    status_code=404,
                    detail="Order not found"
                )

            payment = Payment(
                user_id=payment_data.user_id,
                order_id=payment_data.order_id,
                payment_method=payment_data.payment_method,
                amount=order.total_price
            )

            db.add(payment)

            await db.commit()
            await db.refresh(payment)

            return {
                "message": "Payment created successfully",
                "payment_id": payment.id
            }

        except Exception as e:
            print("========== ERROR ==========")
            print(str(e))
            traceback.print_exc()

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )