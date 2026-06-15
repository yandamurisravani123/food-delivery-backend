from uuid import UUID
 
from app.schemas import dashboard
from app.api.v1.driver.router import dashboard
from app.services.dashboard_service import DashboardService

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.config.database import get_db
from app.core.dependencies import get_current_user, require_super_admin
from app.models.user import User
from app.schemas.delivery import DeliveryAgentOut, MessageResponse
from app.schemas.restaurant import (
    RestaurantApprovalResponse,
    RestaurantOut,
    RestaurantRegisterRequest,
    PendingRestaurantsResponse,
)
from app.services.delivery_service import DeliveryAgentService
from app.services.restaurant_service import RestaurantService
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    OperationsDashboardResponse,
    BusinessKPIDashboardResponse,
    LiveOrdersDashboardResponse,
)
from app.schemas.order_heatmap import OrderHeatmapResponse
from app.services.order_heatmap_service import OrderHeatmapService
 
router = APIRouter(prefix="/Super_admin", tags=["Super Admin"])
 
 
 
 
@router.get("/pending", response_model=PendingRestaurantsResponse)
async def pending_restaurants(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await RestaurantService.get_pending_restaurants(session)
 
 
@router.post("/{restaurant_id}/approve", response_model=RestaurantApprovalResponse)
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
        "message": "Restaurant approved successfully"
    }
 
 
@router.post("/{restaurant_id}/reject", response_model=RestaurantApprovalResponse)
async def reject_restaurant(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    restaurant = await RestaurantService.reject_restaurant(
        session=session,
        restaurant_id=restaurant_id,
        approved_by=current_user.id,
    )
    return {
        "message": "Restaurant rejected successfully",
    }
 
# ==============================
# RESTAURANTS
# ==============================
 
@router.get("/restaurants", response_model=list[RestaurantOut])
async def get_all_restaurants(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    return await RestaurantService.get_all(session)
 
 
@router.get("/restaurants/{restaurant_id}", response_model=RestaurantOut)
async def get_restaurant_by_id(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    return await RestaurantService.get_by_id(
        session,
        restaurant_id,
    )
 
@router.get("/pending-delivery", response_model=list[DeliveryAgentOut])
async def pending_delivery_agents(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    return await DeliveryAgentService.pending_list(session)
 
 
@router.post("/{delivery_agent_id}/approve-delivery", response_model=MessageResponse)
async def approve_delivery_agent(
    delivery_agent_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_super_admin),
):
    await DeliveryAgentService.approve_delivery_agent(
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
    await DeliveryAgentService.reject_delivery_agent(
        session=session,
        delivery_agent_id=delivery_agent_id,
        approved_by=current_user.id,
    )
 
    return {
        "message": "Delivery agent rejected successfully"
    }
 
# ==============================
# DELIVERY AGENTS
# ==============================
 
@router.get("/delivery-agents", response_model=list[DeliveryAgentOut])
async def get_all_delivery_agents(
    session: AsyncSession = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    return await DeliveryAgentService.get_all_delivery_agents(session)
 
 
@router.get("/delivery-agents/{delivery_agent_id}", response_model=DeliveryAgentOut)
async def get_delivery_agent_by_id(
    delivery_agent_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(require_super_admin),
):
    return await DeliveryAgentService.get_delivery_agent_by_id(
        session,
        delivery_agent_id,
    )
# ==========================
# OPERATIONS DASHBOARD
# ==========================

@router.get("/dashboard/operations")
async def get_operations_dashboard(
    db: AsyncSession = Depends(get_db)
):
   return await DashboardService.get_operations_dashboard(db)

# ==========================
# BUSINESS KPI DASHBOARD
# ==========================

@router.get(
    "/dashboard/business-kpi",
    response_model=BusinessKPIDashboardResponse
)
async def get_business_kpi_dashboard(
    db: AsyncSession = Depends(get_db)
):
    return await DashboardService.get_business_kpi_dashboard(db)
# ==========================
# LIVE ORDERS DASHBOARD
# ==========================

@router.get(
    "/dashboard/live-orders",
    response_model=LiveOrdersDashboardResponse
)
async def get_live_orders_dashboard(
    db: AsyncSession = Depends(get_db)
):
    return await DashboardService.get_live_orders_dashboard(db)
#===================================
# order heatmap
#===================================
@router.get(
    "/heatmap",
    response_model=OrderHeatmapResponse,
)
async def get_order_heatmap(
    db: AsyncSession = Depends(get_db),
):
    return await OrderHeatmapService.get_heatmap(db)