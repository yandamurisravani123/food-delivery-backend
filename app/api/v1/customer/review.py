from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File
)

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from app.config.database import get_db

from app.schemas.review import (
    RestaurantReviewRequest
)

from app.services.review_service import (
    ReviewService
)

router = APIRouter()


@router.get("/orders/{order_id}")
async def get_order_details(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await ReviewService.get_order_details(
        db,
        order_id
    )


@router.post("/reviews/restaurant")
async def submit_restaurant_review(
    request: RestaurantReviewRequest,
    db: AsyncSession = Depends(get_db)
):
    return await ReviewService.submit_restaurant_review(
        db,
        request
    )


@router.post("/reviews/photos/upload")
async def upload_review_photos(
    order_id: str,
    photos: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    return await ReviewService.upload_review_photos(
        db,
        order_id,
        photos
    )


@router.delete("/reviews/photos/{photo_id}")
async def delete_review_photo(
    photo_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await ReviewService.delete_review_photo(
        db,
        photo_id
    )


@router.get("/reviews/delivery/{order_id}")
async def get_delivery_feedback(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await ReviewService.get_delivery_feedback(
        db,
        order_id
    )


@router.get("/reviews/status/{order_id}")
async def check_review_status(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await ReviewService.check_review_status(
        db,
        order_id
    )