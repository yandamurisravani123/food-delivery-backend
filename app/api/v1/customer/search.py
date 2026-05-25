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

from app.services.search_service import (
    SearchService
)

router = APIRouter(
    prefix="/customer",
    tags=["Search"]   # ← ADD THIS ONLY
)


@router.get("/search")
async def search_restaurants(
    keyword: str = Query(...),
    db: AsyncSession = Depends(get_db)
):

    return await SearchService.search_restaurants(
        keyword,
        db
    )