from fastapi import APIRouter

from app.schemas.payment import (
    PaymentRequest,
    PaymentResponse
)

from app.services.payment_service import PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# ==========================
# CREATE PAYMENT
# ==========================
@router.post(
    "/pay",
)
async def make_payment(payload: PaymentRequest):

    result = await PaymentService.create_payment(payload)

    return result