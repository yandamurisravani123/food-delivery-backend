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
    prefix="/api/v1/customer/home",
    tags=["Home Feed"]
)


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


@router.get("/picked")
async def picked_for_you(
    db: AsyncSession = Depends(get_db)
):

    return await (
        HomeFeedService
        .picked_for_you(db)
    )


@router.get("/cuisines")
async def cuisines():

    return await (
        HomeFeedService
        .cuisines()
    )


@router.get("/popular")
async def popular_near_you(
    db: AsyncSession = Depends(get_db)
):

    return await (
        HomeFeedService
        .popular_near_you(db)
    )