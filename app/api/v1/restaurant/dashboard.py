from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.config.database import get_db
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import DashboardSummaryResponse
from app.models.order import Order


router = APIRouter(
    prefix="/restaurant/dashboard",
)


@router.get("/metrics")
async def get_metrics(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.get_metrics(session, restaurant_id)


@router.get("/repeat-orders")
async def get_repeat_orders(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.repeat_orders(session, restaurant_id)


@router.get("/market-reach")
async def get_market_reach(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.market_reach(session, restaurant_id)


@router.get("/rating-trend")
async def get_rating_trend(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.rating_trend(session, restaurant_id)


@router.get("/growth-tips")
async def growth_tips(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.growth_tips(session, restaurant_id)


@router.get("/competitor-benchmark")
async def competitor_benchmark(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.competitor_benchmark(session, restaurant_id)


@router.get("/marketing-impact")
async def marketing_impact(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.marketing_impact(session, restaurant_id)


@router.get("/stock-efficiency")
async def stock_efficiency(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.stock_efficiency(session, restaurant_id)


@router.get("/staff-performance")
async def staff_performance(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.staff_performance(session, restaurant_id)





@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
async def dashboard_summary(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):

    return await DashboardService.dashboard_summary(
        session,
        restaurant_id
    )