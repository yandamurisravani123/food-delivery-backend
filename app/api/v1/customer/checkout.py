from fastapi import APIRouter

from app.services.checkout_service import (
    CheckoutService
)

router = APIRouter()


@router.post("/cart/checkout-preview")
async def checkout_preview():

    return await CheckoutService.checkout_preview()