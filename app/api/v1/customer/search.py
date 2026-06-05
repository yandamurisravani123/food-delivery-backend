from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.services.customer_discovery_service import CustomerDiscoveryService

router = APIRouter(
    prefix="/customer",
    tags=["Search"]
)


@router.get("/search")
async def search_restaurants(
    query: str = Query(..., min_length=1, description="Search keyword for restaurant name or city"),
    db: AsyncSession = Depends(get_db)
):
<<<<<<< HEAD
    return await CustomerDiscoveryService.search(
        db=db,
        query=keyword
=======
    return await SearchService.search_restaurants(
        keyword=query,
        db=db
>>>>>>> 4182889fcc5f5551fc633147132415f45bd34f84
    )