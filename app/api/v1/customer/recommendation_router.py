from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.food import Food
from app.models.user_preference import UserPreference
from uuid import UUID

router = APIRouter(
    prefix="/recommendations",
    tags=["AI Recommendations"]
)


@router.get("/{user_id}")
async def ai_recommendations(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    # FETCH USER PREFERENCE
    preference_result = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == user_id
        )
    )

    preference = preference_result.scalar()

    if not preference:
        raise HTTPException(
            status_code=404,
            detail="User preference not found"
        )

    # FETCH FOODS MATCHING CUISINE
    food_result = await db.execute(
        select(Food).where(
            Food.cuisine == preference.favorite_cuisine
        )
    )

    foods = food_result.scalars().all()

    return {
        "user_id": user_id,
        "favorite_cuisine": preference.favorite_cuisine,
        "recommendations": foods
    }