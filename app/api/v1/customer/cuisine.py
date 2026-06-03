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

from app.services.cuisine_service import (
    CuisineService
)

router = APIRouter(
    prefix="/customer/cuisine",
)


@router.get("/")
async def get_cuisines(
    db: AsyncSession = Depends(get_db)
):

    return await CuisineService.get_cuisines(
        db
    )