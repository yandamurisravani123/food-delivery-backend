from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.order_tracking import (
    UpdateLocationSchema
)
from app.services.order_tracking_service import (
    OrderTrackingService
)

router = APIRouter(
    prefix="/order-tracking",
    tags=["Order Tracking"]
)


@router.get("/{order_id}")
async def get_order_tracking(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):
    order = await (
        OrderTrackingService
        .get_tracking(
            db,
            order_id
        )
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@router.patch("/{order_id}/location")
async def update_driver_location(
    order_id: str,
    request: UpdateLocationSchema,
    db: AsyncSession = Depends(get_db)
):
    tracking = await (
        OrderTrackingService
        .update_location(
            db,
            order_id,
            request.latitude,
            request.longitude
        )
    )

    return {
        "message":
        "Driver location updated",
        "data": tracking
    }