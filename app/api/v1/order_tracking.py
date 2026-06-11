from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from uuid import UUID
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
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await (
        OrderTrackingService
        .get_tracking(
            db,
            order_id
        )
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order, tracking = result

    return {
        "order_id": str(order.id),
        "user_id": str(order.user_id),
        "restaurant_id": str(order.restaurant_id),
        "status": order.status,
        "delivery_address": order.delivery_address,
        "courier_name": order.courier_name,
        "courier_rating": order.courier_rating,
        "special_instructions": order.special_instructions,
        "cutlery_required": order.cutlery_required,
        "subtotal": order.subtotal,
        "delivery_fee": order.delivery_fee,
        "tax_percent": order.tax_percent,
        "total": order.total,
        "order_time": order.order_time,
        "created_at": order.created_at,
        "tracking": {
            "id": str(tracking.id),
            "order_id": str(tracking.order_id),
            "delivery_partner_id": str(tracking.delivery_partner_id),
            "status": tracking.status,
            "created_at": tracking.created_at
        }
    }


@router.patch("/{order_id}/location")
async def update_driver_location(
    order_id: UUID,
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
        "message": "Driver location updated",
        "data": tracking
    }