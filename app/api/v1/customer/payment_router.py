from fastapi import APIRouter

from app.schemas.payment import PaymentRequest
from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.post("/pay")
def make_payment(payment: PaymentRequest):
    return PaymentService.create_payment(payment)