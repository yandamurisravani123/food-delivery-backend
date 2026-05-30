from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.config.database import get_db
from app.schemas.ratings_schema import (
    RatingCreate,
    RatingResponse,
    MessageResponse
    
)
from app.services.rating_service import RatingService


router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


@router.post(
    "/create",
    response_model=RatingResponse
)
async def create_rating(
    payload: RatingCreate,
    db: AsyncSession = Depends(get_db)
):
    return await RatingService.create_rating(
        db,
        payload
    )


@router.get(
    "/all",
    response_model=List[RatingResponse]
)
async def get_ratings(
    db: AsyncSession = Depends(get_db)
):
    return await RatingService.get_all_ratings(db)