from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.config.database import get_db
from app.models.food import Food
from app.models.user_preference import UserPreference
from uuid import UUID
import uuid

router = APIRouter(
    prefix="/recommendations",
    tags=["AI Recommendations"]
)


# ── Pydantic schema ──────────────────────────────────────────
class UserPreferenceCreate(BaseModel):
    user_id: UUID
    favorite_cuisine: str
    spicy_level: str
    preferred_food_type: str


# ── POST - Create user preference ────────────────────────────
@router.post("/preferences")
async def create_user_preference(
    data: UserPreferenceCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if preference already exists
    result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == data.user_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Preference already exists for this user")

    preference = UserPreference(
        id=uuid.uuid4(),
        user_id=data.user_id,
        favorite_cuisine=data.favorite_cuisine,
        spicy_level=data.spicy_level,
        preferred_food_type=data.preferred_food_type
    )

    db.add(preference)
    await db.commit()
    await db.refresh(preference)

    return {
        "message": "Preference created successfully",
        "data": {
            "id": str(preference.id),
            "user_id": str(preference.user_id),
            "favorite_cuisine": preference.favorite_cuisine,
            "spicy_level": preference.spicy_level,
            "preferred_food_type": preference.preferred_food_type
        }
    }


# ── GET - Get recommendations ────────────────────────────────
@router.get("/{user_id}")
async def ai_recommendations(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    # Fetch user preference
    preference_result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == user_id)
    )
    preference = preference_result.scalar()

    if not preference:
        raise HTTPException(status_code=404, detail="User preference not found")

    # Fetch foods matching cuisine
    food_result = await db.execute(
        select(Food).where(Food.cuisine == preference.favorite_cuisine)
    )
    foods = food_result.scalars().all()

    return {
        "user_id": user_id,
        "favorite_cuisine": preference.favorite_cuisine,
        "recommendations": foods
    }