from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db

from app.schemas.payment_method import (
    PaymentMethodCreate,
    PaymentMethodUpdate
)

from app.services.payment_method_service import (
    PaymentMethodService
)

router = APIRouter(
    prefix="/api/v1/payment-method",
    tags=["Payment Method"]
)


@router.post("/create")
async def create_payment_method(
    data: PaymentMethodCreate,
    db: AsyncSession = Depends(get_db)
):
    return await PaymentMethodService.create_payment_method(
        db,
        data
    )


@router.get("/customer/{customer_id}")
async def customer_payments(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await PaymentMethodService.get_customer_payments(
        db,
        customer_id
    )


@router.get("/all")
async def all_payments(
    db: AsyncSession = Depends(get_db)
):
    return await PaymentMethodService.get_all_payments(
        db
    )


@router.get("/{payment_method_id}")
async def get_payment_method(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    payment = await PaymentMethodService.get_payment_method(
        db,
        payment_method_id
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )

    return payment


@router.patch("/update/{payment_method_id}")
async def update_payment(
    payment_method_id: UUID,
    data: PaymentMethodUpdate,
    db: AsyncSession = Depends(get_db)
):
    payment = await PaymentMethodService.get_payment_method(
        db,
        payment_method_id
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )

    return await PaymentMethodService.update_payment_method(
        db,
        payment,
        data
    )


@router.delete("/delete/{payment_method_id}")
async def delete_payment(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    payment = await PaymentMethodService.get_payment_method(
        db,
        payment_method_id
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment method not found"
        )

    await PaymentMethodService.delete_payment_method(
        db,
        payment
    )

    return {"message": "Deleted successfully"}


@router.post("/set-default/{payment_method_id}")
async def set_default(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    payment = await PaymentMethodService.get_payment_method(
        db,
        payment_method_id
    )

    await PaymentMethodService.set_default(
        db,
        payment
    )

    return {"message": "Default updated"}


@router.patch("/activate/{payment_method_id}")
async def activate_payment(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    payment = await PaymentMethodService.get_payment_method(
        db,
        payment_method_id
    )

    await PaymentMethodService.activate(
        db,
        payment
    )

    return {"message": "Activated"}


@router.patch("/deactivate/{payment_method_id}")
async def deactivate_payment(
    payment_method_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    payment = await PaymentMethodService.get_payment_method(
        db,
        payment_method_id
    )

    await PaymentMethodService.deactivate(
        db,
        payment
    )

    return {"message": "Deactivated"}