from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.core.dependencies import require_super_admin
from app.models.user import User

from app.schemas.driver import DriverOut, MessageResponse
from app.schemas.restaurant import (
    RestaurantApprovalResponse,
    RestaurantOut,
)

from app.services.driver_service import DriverService
from app.services.restaurant_service import RestaurantService


router = APIRouter(
    prefix="/Super_admin",
    tags=["Super Admin"]
)


# ==============================
# PENDING RESTAURANTS
# ==============================

@router.get("/pending", response_model=list[RestaurantOut])
async def pending_restaurants(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await RestaurantService.get_pending_restaurants(session)


@router.post("/{restaurant_id}/approve")
async def approve_restaurant(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    restaurant = await RestaurantService.approve_restaurant(
        session=session,
        restaurant_id=restaurant_id,
        approved_by=current_user.id,
    )

    return {
        "message": "Restaurant approved successfully",
        "restaurant_id": str(restaurant_id)
    }


@router.post("/{restaurant_id}/reject", response_model=RestaurantApprovalResponse)
async def reject_restaurant(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    await RestaurantService.reject_restaurant(
        session=session,
        restaurant_id=restaurant_id,
        approved_by=current_user.id,
    )

    return {
        "message": "Restaurant rejected successfully"
    }


# ==============================
# RESTAURANTS
# ==============================

@router.get("/restaurants", response_model=list[RestaurantOut])
async def get_all_restaurants(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await RestaurantService.get_all(session)


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantOut)
async def get_restaurant_by_id(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await RestaurantService.get_by_id(
        session,
        restaurant_id,
    )


# ==============================
# DELIVERY AGENTS
# ==============================

@router.get("/pending-delivery", response_model=list[DriverOut])
async def pending_delivery_agents(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await DriverService.pending_list(session)


@router.post("/{delivery_agent_id}/approve-delivery", response_model=MessageResponse)
async def approve_delivery_agent(
    delivery_agent_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    await DriverService.approve_delivery_agent(
        session=session,
        delivery_agent_id=delivery_agent_id,
        approved_by=current_user.id,
    )

    return {
        "message": "Delivery agent approved successfully"
    }


@router.post("/{delivery_agent_id}/reject-delivery", response_model=MessageResponse)
async def reject_delivery_agent(
    delivery_agent_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    await DriverService.reject_delivery_agent(
        session=session,
        delivery_agent_id=delivery_agent_id,
        approved_by=current_user.id,
    )

    return {
        "message": "Delivery agent rejected successfully"
    }


@router.get("/delivery-agents", response_model=list[DriverOut])
async def get_all_delivery_agents(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await DriverService.get_all_delivery_agents(session)


@router.get("/delivery-agents/{delivery_agent_id}", response_model=DriverOut)
async def get_delivery_agent_by_id(
    delivery_agent_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await DriverService.get_delivery_agent_by_id(
        session,
        delivery_agent_id,
    )