from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.dependencies import (
    get_db
)

from app.services.filter_service import (
    FilterService
)

router = APIRouter(
    prefix="/customer/filter",
    tags=["Filter"]
)


@router.get("/")
async def filter_restaurants(
    cuisine: str = Query(None),
    rating: float = Query(None),
    db: AsyncSession = Depends(get_db)
):

    return await FilterService.filter_restaurants(
        db,
        cuisine,
        rating
    )