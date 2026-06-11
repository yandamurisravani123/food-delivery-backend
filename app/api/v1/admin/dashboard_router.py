from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.services.dashboard_service import (
    DashboardService
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/operations")
async def operations_dashboard(
    db: AsyncSession = Depends(get_db)
):
    return await DashboardService.get_operations_dashboard(
        db
    )


@router.get("/kpi")
async def kpi_dashboard(
    db: AsyncSession = Depends(get_db)
):
    return await DashboardService.get_kpi_dashboard(
        db
    )


@router.get("/live-orders")
async def live_orders_dashboard(
    db: AsyncSession = Depends(get_db)
):
    return await DashboardService.get_live_orders(
        db
    )