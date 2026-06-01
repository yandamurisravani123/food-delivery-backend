from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.models.feedback import Feedback
from app.models.user import User

from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackSuccessResponse
)

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"]
)


@router.post(
    "/create",
    response_model=FeedbackSuccessResponse
)
async def create_feedback(
    payload: FeedbackCreate,
    db: AsyncSession = Depends(get_db)
):

    user_result = await db.execute(
        select(User).where(
            User.id == payload.user_id
        )
    )

    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    feedback = Feedback(
        user_id=payload.user_id,
        order_id=payload.order_id,
        rating=payload.rating,
        review=payload.review,
        reward_points=15
    )

    db.add(feedback)

    user.reward_points = (
        user.reward_points or 0
    ) + 15

    await db.commit()

    return {
        "message": "Thank you for your feedback!",
        "experience_rating": payload.rating,
        "reward_points_earned": 15
    }