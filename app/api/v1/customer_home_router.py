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


# ==========================
# tracking
# ==========================
from fastapi import APIRouter

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)


@router.get("/tracking")
def tracking():

    return {
        "message": "Tracking API Working"
    }


@router.get("/notifications")
def get_notifications():

    return {
        "notifications": [
            {
                "title": "Order Confirmed",
                "message": "Your order has been confirmed"
            },
            {
                "title": "Out For Delivery",
                "message": "Delivery partner is on the way"
            }
        ]
    }

from fastapi import APIRouter
from app.schemas.payment import PaymentRequest
from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/pay")
def make_payment(payment: PaymentRequest):

    response = PaymentService.create_payment(payment)

    return response

# ==========================
# notification
# ==========================
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.notification import (
    NotificationCreateSchema,
    NotificationResponseSchema
)

from app.services.notification_service import (
    NotificationService
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post(
    "/create",
    response_model=NotificationResponseSchema
)
async def create_notification(
    data: NotificationCreateSchema,
    db: AsyncSession = Depends(get_db)
):

    notification = await NotificationService.create_notification(
        db,
        data
    )

    return notification


@router.get(
    "/user/{user_id}",
    response_model=list[NotificationResponseSchema]
)
async def get_notifications(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):

    notifications = await NotificationService.get_notifications(
        db,
        user_id
    )

    return notifications