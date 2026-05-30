from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.refund import (
    RefundCreate,
    RefundStatusUpdate
)

from app.services.refund_service import RefundService

router = APIRouter(prefix="/refund", tags=["Refund"])


@router.post("/initiate")
async def initiate_refund(
    payload: RefundCreate,
    db: AsyncSession = Depends(get_db)
):

    return await RefundService.initiate_refund(
        db,
        payload
    )


@router.get("/{order_id}")
async def get_refund(
    order_id,
    db: AsyncSession = Depends(get_db)
):

    return await RefundService.get_refund(
        db,
        order_id
    )