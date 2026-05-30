from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.payment import PaymentSchema

from app.services.payment_service import PaymentService


router = APIRouter(
    prefix="/api/v1/payments",
    tags=["Payments"]
)


@router.post("/pay")
async def make_payment(
    payload: PaymentSchema,
    db: AsyncSession = Depends(get_db)
):

    return await PaymentService.make_payment(
        db,
        payload
    )