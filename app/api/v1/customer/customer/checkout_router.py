from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.checkout import (
    CheckoutCreate,
    CheckoutResponse
)

from app.services.checkout_service import CheckoutService


router = APIRouter(
    prefix="/api/v1/checkout",
    tags=["Checkout"]
)


@router.post(
    "/schedule-order",
    response_model=CheckoutResponse
)
async def schedule_order(
    payload: CheckoutCreate,
    db: AsyncSession = Depends(get_db)
):

    return await CheckoutService.create_checkout(
        db,
        payload
    )