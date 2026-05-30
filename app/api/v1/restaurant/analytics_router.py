from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.services.analytics_service import (

    get_top_selling_by_quantity,

    get_top_selling_by_revenue,

    get_category_insights,

    get_menu_rankings,

    get_dashboard_data
)

# ROUTER

router = APIRouter(

    prefix="/restaurants/analytics",
)

# COMPLETE DASHBOARD

@router.get("/dashboard/{restaurant_id}")
async def dashboard(

    restaurant_id: str,

    db: AsyncSession = Depends(get_db)
):

    data = await get_dashboard_data(
        db,
        restaurant_id
    )

    return data

# TOP SELLING ITEMS

@router.get("/top-selling/{restaurant_id}")
async def top_selling(

    restaurant_id: str,

    db: AsyncSession = Depends(get_db)
):

    data = await get_top_selling_by_quantity(
        db,
        restaurant_id
    )

    return data

# TOP REVENUE ITEMS

@router.get("/top-revenue/{restaurant_id}")
async def top_revenue(

    restaurant_id: str,

    db: AsyncSession = Depends(get_db)
):

    data = await get_top_selling_by_revenue(
        db,
        restaurant_id
    )

    return data

# CATEGORY INSIGHTS

@router.get("/category-insights/{restaurant_id}")
async def category_insights(

    restaurant_id: str,

    db: AsyncSession = Depends(get_db)
):

    data = await get_category_insights(
        db,
        restaurant_id
    )

    return data

# MENU RANKINGS

@router.get("/menu-rankings/{restaurant_id}")
async def menu_rankings(

    restaurant_id: str,

    db: AsyncSession = Depends(get_db)
):

    data = await get_menu_rankings(
        db,
        restaurant_id
    )

    return data