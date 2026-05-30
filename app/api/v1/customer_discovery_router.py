from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.services.customer_discovery_service import (
    CustomerDiscoveryService
)

router = APIRouter(
    prefix="/api/v1/customer",
    tags=["Customer Discovery"]
)


# SEARCH
@router.get("/search")
async def search(
    query: str,
    db: AsyncSession = Depends(get_db)
):

    return await CustomerDiscoveryService.search(
        db=db,
        query=query
    )


# CUISINE FILTER
@router.get("/cuisine/{cuisine}")
async def cuisine_filter(
    cuisine: str,
    db: AsyncSession = Depends(get_db)
):

    return await (
        CustomerDiscoveryService
        .cuisine_filter(
            db=db,
            cuisine=cuisine
        )
    )


# TRENDING RESTAURANTS
@router.get("/trending")
async def trending_restaurants(
    db: AsyncSession = Depends(get_db)
):

    return await (
        CustomerDiscoveryService
        .trending_restaurants(db)
    )


# TOP RATED RESTAURANTS
@router.get("/top-rated")
async def top_rated_restaurants(
    db: AsyncSession = Depends(get_db)
):

    return await (
        CustomerDiscoveryService
        .top_rated(db)
    )


