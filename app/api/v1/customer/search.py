from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/customer",
    tags=["Search"]
)


@router.get("/search")
async def search_restaurants(
<<<<<<< HEAD
    query: str = Query(..., min_length=1, description="Search keyword for restaurant name or city"),
=======
    keyword: str = Query(..., alias="query", min_length=1, description="Search keyword for restaurant name or city"),
>>>>>>> 9bdccde6702a1a094a887e8eb2d6daaa034bb150
    db: AsyncSession = Depends(get_db)
):
    return await SearchService.search_restaurants(
        keyword=query,
        db=db
    )