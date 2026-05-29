from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.rating_schema import (
    RatingCreate,
    RatingResponse
)

from app.services.rating_service import (
    RatingService
)

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


@router.post(
    "/submit",
    response_model=RatingResponse
)
async def submit_rating(
    payload: RatingCreate,
    db: AsyncSession = Depends(get_db)
):

    return await RatingService.create_rating(
        db,
        payload
    )


@router.get("/driver/{driver_id}")
async def get_driver_ratings(
    driver_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await RatingService.get_driver_ratings(
        db,
        driver_id
    )