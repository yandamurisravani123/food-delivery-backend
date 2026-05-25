from fastapi import (
    APIRouter,
    Depends,
    Body
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.dependencies import (
    get_db
)

from app.services.recent_search_service import (
    RecentSearchService
)

router = APIRouter(
    prefix="/customer/recent-search",
)


@router.get("/")
async def get_recent_searches(
    db: AsyncSession = Depends(get_db)
):

    return await RecentSearchService.get_recent_searches(
        db
    )


@router.post("/")
async def add_recent_search(
    keyword: str = Body(...),
    db: AsyncSession = Depends(get_db)
):

    return await RecentSearchService.add_recent_search(
        keyword,
        db
    )


@router.delete("/clear/all")
async def clear_recent_searches(
    db: AsyncSession = Depends(get_db)
):

    return await RecentSearchService.clear_recent_searches(
        db
    )