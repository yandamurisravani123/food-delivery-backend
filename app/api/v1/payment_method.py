from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db
from app.models.payment import Payment
from app.schemas.payment import (
    PaymentRequest,
    PaymentResponse
)
from app.services.payment_method_service import PaymentMethodService
from app.schemas.payment_method import PaymentMethodUpdate

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

