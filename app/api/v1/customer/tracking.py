from uuid import UUID

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.dependencies import (
    get_db
)

from app.services.tracking_service import (
    TrackingService
)

from app.schemas.tracking_schema import (
    UpdateLocationRequest,
    UpdateStatusRequest
)

router = APIRouter(
    prefix="/tracking",
    tags=["Tracking"]
)


@router.get("/{order_id}")
async def get_tracking(
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await TrackingService.get_tracking(
        db,
        order_id
    )


@router.post("/{order_id}/location")
async def update_location(
    order_id: UUID,
    delivery_partner_id: UUID,
    request: UpdateLocationRequest,
    db: AsyncSession = Depends(get_db)
):

    return await TrackingService.update_location(
        db,
        order_id,
        delivery_partner_id,
        request.latitude,
        request.longitude
    )


@router.put("/{order_id}/status")
async def update_status(
    order_id: UUID,
    delivery_partner_id: UUID,
    request: UpdateStatusRequest,
    db: AsyncSession = Depends(get_db)
):

    return await TrackingService.update_status(
        db,
        order_id,
        delivery_partner_id,
        request.status
    )