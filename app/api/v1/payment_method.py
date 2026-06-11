from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.payment import Payment
from app.schemas.payment import (
    PaymentRequest,
    PaymentResponse
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/create",
    response_model=PaymentResponse
)
async def create_payment(
    payload: PaymentRequest,
    db: AsyncSession = Depends(get_db)
):
    payment = Payment(
        order_id=payload.order_id,
        amount=payload.amount,
        payment_type=payload.payment_type,
        status=payload.status.value
    )

    db.add(payment)

    await db.commit()

    await db.refresh(payment)

    return PaymentResponse(
        message="Payment created successfully",
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payload.payment_method,
        status=payload.status
    )