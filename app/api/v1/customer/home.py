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

from app.services.home_service import (
    HomeService
)

router = APIRouter(
    prefix="/customer",
    # tags=["customer"]
)


@router.get("/home")
async def get_home(
    db: AsyncSession = Depends(get_db)
):

    return await HomeService.get_home_data(
        db
    )