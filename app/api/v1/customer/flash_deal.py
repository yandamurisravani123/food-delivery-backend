from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.dependencies import (
    get_db
)

from app.services.flash_deal_service import (
    FlashDealService
)

router = APIRouter(
    prefix="/customer/flash-deals",
    tags=["Flash Deals"]
)


@router.get("/")
async def get_flash_deals(
    db: AsyncSession = Depends(get_db)
):

    return await FlashDealService.get_flash_deals(
        db
    )