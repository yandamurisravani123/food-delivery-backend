from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.services.order_preparation_service import OrderPreparationService

router = APIRouter(prefix="/orders", tags=["Order Preparation"])


# ✅ GET ORDER PREPARATION SCREEN
@router.get("/{order_id}/preparation")
async def get_preparation(order_id: int, db: AsyncSession = Depends(get_db)):
    return await OrderPreparationService.get_preparation(db, order_id)


# ✅ UPDATE CHEF PROGRESS (75%, cooking, QC etc.)
@router.patch("/{order_id}/preparation")
async def update_preparation(
    order_id: int,
    stage: str,
    progress: int,
    note: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    return await OrderPreparationService.update_preparation(
        db, order_id, stage, progress, note
    )