from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from app.config.database import get_db
from app.schemas.payment import PaymentRequest
from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)


@router.post("/select-method")
async def select_payment_method(
    payment_data: PaymentRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        payment = await PaymentService.select_payment_method(
            db=db,
            payment_data=payment_data
        )

        return payment

    except Exception as e:
        print("========= FULL ERROR =========")
        print(str(e))
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )