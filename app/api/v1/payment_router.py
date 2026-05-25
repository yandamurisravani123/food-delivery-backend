from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.config.database import (
    get_db
)

from app.schemas.payment import (
    CODPaymentSchema
)

from app.services.payment_service import (
    PaymentService
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# =========================
# CASH ON DELIVERY API
# =========================

@router.post("/cod")
async def cash_on_delivery(
    payload: CODPaymentSchema,
    db: AsyncSession = Depends(get_db)
):

    return await PaymentService.cash_on_delivery(
        db,
        payload
    )