from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db
from app.schemas.ratings_schema import (
    RatingCreate,
    RatingResponse
)
from app.services.rating_service import RatingService

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


@router.post(
    "/review",
    response_model=RatingResponse
)
async def submit_review(
    data: RatingCreate,
    db: AsyncSession = Depends(get_db)
):
    return await RatingService.create_review(
        db,
        data
    )


@router.get("/order/{order_id}")
async def get_order_review(
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await RatingService.get_order_review(
        db,
        order_id
    )


@router.get("/driver/{driver_id}")
async def get_driver_reviews(
    driver_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await RatingService.get_driver_reviews(
        db,
        driver_id
    )