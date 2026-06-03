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

from app.services.offer_service import (
    OfferService
)

router = APIRouter(
    prefix="/customer/offers",
    tags=["Offers"]
)


@router.get("/")
async def get_offers(
    db: AsyncSession = Depends(get_db)
):

    return await OfferService.get_offers(
        db
    )