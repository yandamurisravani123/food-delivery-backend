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

from app.services.map_service import (
    MapService
)

router = APIRouter(
    prefix="/customer/map",
    tags=["Map"]
)


@router.get("/restaurants")
async def get_map_restaurants(
    db: AsyncSession = Depends(get_db)
):

    return await MapService.get_restaurants(
        db
    )