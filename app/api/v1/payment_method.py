from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db
from app.schemas.payment_method import (
    PaymentMethodCreate,
    PaymentMethodUpdate
)
from app.services.payment_method_service import PaymentMethodService


router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment Methods"]
)


# --------------------------------
# CREATE PAYMENT METHOD
# --------------------------------
@router.post("/")
async def create_payment_method(
    data: PaymentMethodCreate,
    db: AsyncSession = Depends(get_db)
):
    payment = await PaymentMethodService.create_payment_method(
        db, data
    )
    return {
        "message": "Payment method created",
        "data": payment
    }


# --------------------------------
# GET ALL PAYMENT METHODS
# --------------------------------
@router.get("/")
async def get_all_payment_methods(
    db: AsyncSession = Depends(get_db)
):
    methods = await PaymentMethodService.get_all_payments(db)
    return {"payment_methods": methods}


# --------------------------------
# GET BY CUSTOMER
# --------------------------------
@router.get("/customer/{customer_id}")
async def get_customer_payment_methods(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    methods = await PaymentMethodService.get_customer_payments(
        db, customer_id
    )
    return {"payment_methods": methods}


# --------------------------------
# GET BY ID
# --------------------------------
@router.get("/{payment_method_id}")
async def get_payment_method(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    method = await PaymentMethodService.get_payment_method(
        db, payment_method_id
    )
    if not method:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )
    return method


# --------------------------------
# UPDATE PAYMENT METHOD
# --------------------------------
@router.put("/{payment_method_id}")
async def update_payment_method(
    payment_method_id: UUID,
    data: PaymentMethodUpdate,
    db: AsyncSession = Depends(get_db)
):
    method = await PaymentMethodService.get_payment_method(
        db, payment_method_id
    )
    if not method:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )
    updated = await PaymentMethodService.update_payment_method(
        db, method, data
    )
    return {
        "message": "Payment method updated",
        "data": updated
    }


# --------------------------------
# SET DEFAULT
# --------------------------------
@router.patch("/{payment_method_id}/set-default")
async def set_default_payment_method(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    method = await PaymentMethodService.get_payment_method(
        db, payment_method_id
    )
    if not method:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )
    await PaymentMethodService.set_default(db, method)
    return {"message": "Default payment method updated"}


# --------------------------------
# ACTIVATE
# --------------------------------
@router.patch("/{payment_method_id}/activate")
async def activate_payment_method(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    method = await PaymentMethodService.get_payment_method(
        db, payment_method_id
    )
    if not method:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )
    await PaymentMethodService.activate(db, method)
    return {"message": "Payment method activated"}


# --------------------------------
# DEACTIVATE
# --------------------------------
@router.patch("/{payment_method_id}/deactivate")
async def deactivate_payment_method(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    method = await PaymentMethodService.get_payment_method(
        db, payment_method_id
    )
    if not method:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )
    await PaymentMethodService.deactivate(db, method)
    return {"message": "Payment method deactivated"}


# --------------------------------
# DELETE PAYMENT METHOD
# --------------------------------
@router.delete("/{payment_method_id}")
async def delete_payment_method(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    method = await PaymentMethodService.get_payment_method(
        db, payment_method_id
    )
    if not method:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )
    await PaymentMethodService.delete_payment_method(db, method)
    return {"message": "Payment method deleted"}