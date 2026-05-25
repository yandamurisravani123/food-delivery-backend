from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from uuid import UUID

from app.core.dependencies import (
    get_db
)

from app.services.restaurant_service import (
    RestaurantService
)

router = APIRouter(
    prefix="/customer/restaurant",
    tags=["Customer Restaurant"]
)


# ==========================================
# Get Restaurant By ID
# ==========================================

@router.get("/{restaurant_id}")
async def get_restaurant(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await RestaurantService.get_by_id(
        db,
        restaurant_id
    )


# ==========================================
# Nearby Restaurants
# ==========================================

@router.get("/nearby/list")
async def nearby_restaurants(
    db: AsyncSession = Depends(get_db)
):

    return await RestaurantService.nearby_restaurants(
        db
    )


# ==========================================
# Restaurant Menu
# ==========================================

@router.get("/{restaurant_id}/menu")
async def get_restaurant_menu(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await RestaurantService.restaurant_menu(
        db,
        restaurant_id
    )


# ==========================================
# Restaurant Reviews
# ==========================================

@router.get("/{restaurant_id}/reviews")
async def get_restaurant_reviews(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await RestaurantService.restaurant_reviews(
        db,
        restaurant_id
    )