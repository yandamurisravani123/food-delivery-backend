from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.config.database import (
    get_db
)

from app.services.home_feed_service import (
    HomeFeedService
)

router = APIRouter(
    prefix="/api/v1/home-feed",
    tags=["Home Feed"]
)


# ==========================
# COMPLETE HOME FEED
# ==========================
@router.get("/")
async def home_feed(
    customer_id: str = None,
    db: AsyncSession = Depends(get_db)
):

    return await (
        HomeFeedService.home_feed(
            db=db,
            customer_id=customer_id
        )
    )


# ==========================
# BANNERS
# ==========================
@router.get("/banners")
async def banners():

    return await (
        HomeFeedService.banners()
    )


# ==========================
# PICKED FOR YOU
# ==========================
@router.get("/picked")
async def picked_for_you(
    db: AsyncSession = Depends(get_db)
):

    return await (
        HomeFeedService
        .picked_for_you(db)
    )


# ==========================
# POPULAR NEAR YOU
# ==========================
@router.get("/popular")
async def popular_near_you(
    db: AsyncSession = Depends(get_db)
):

    return await (
        HomeFeedService
        .popular_near_you(db)
    )


# ==========================
# TRENDING RESTAURANTS
# ==========================
@router.get("/trending")
async def trending_restaurants(
    db: AsyncSession = Depends(get_db)
):

    return await (
        HomeFeedService
        .trending_restaurants(db)
    )


# ==========================
# CUISINES
# ==========================
@router.get("/cuisines")
async def cuisines():

    return await (
        HomeFeedService
        .cuisines()
    )


# ==========================
# OFFERS
# ==========================
@router.get("/offers")
async def offers():

    return await (
        HomeFeedService
        .offers()
    )


# ==========================
# CART COUNT
# ==========================
@router.get("/cart-count/{customer_id}")
async def cart_count(
    customer_id: str,
    db: AsyncSession = Depends(get_db)
):

    return await (
        HomeFeedService
        .cart_count(
            db=db,
            customer_id=customer_id
        )
    )