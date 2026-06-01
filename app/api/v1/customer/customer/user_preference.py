from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.user_preference import UserPreference

from app.schemas.user_preference import (
    PreferenceCreate,
    PreferenceUpdate
)

from uuid import UUID


router = APIRouter(
    prefix="/preferences",
    tags=["User Preferences"]
)


# CREATE PREFERENCE
@router.post("/")
async def create_preference(
    payload: PreferenceCreate,
    db: AsyncSession = Depends(get_db)
):

    new_preference = UserPreference(
        user_id=payload.user_id,
        favorite_cuisine=payload.favorite_cuisine,
        spicy_level=payload.spicy_level,
        preferred_food_type=payload.preferred_food_type
    )

    db.add(new_preference)

    await db.commit()

    await db.refresh(new_preference)

    return {
        "message": "Preference created successfully",
        "data": new_preference
    }


# GET ALL PREFERENCES
@router.get("/")
async def get_all_preferences(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(UserPreference)
    )

    preferences = result.scalars().all()

    return preferences


# GET USER PREFERENCE
@router.get("/{user_id}")
async def get_user_preference(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(UserPreference).where(
            UserPreference.user_id == user_id
        )
    )

    preference = result.scalar()

    if not preference:
        raise HTTPException(
            status_code=404,
            detail="Preference not found"
        )

    return preference


# UPDATE PREFERENCE
@router.put("/{preference_id}")
async def update_preference(
    preference_id: UUID,
    preference: PreferenceUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(UserPreference).where(
            UserPreference.id == preference_id
        )
    )

    preference = result.scalar()

    if not preference:
        raise HTTPException(
            status_code=404,
            detail="Preference not found"
        )

    preference.favorite_cuisine = payload.favorite_cuisine
    preference.spicy_level = payload.spicy_level
    preference.preferred_food_type = payload.preferred_food_type

    await db.commit()

    await db.refresh(preference)

    return {
        "message": "Preference updated successfully",
        "data": preference
    }


# DELETE PREFERENCE
@router.delete("/{user_id}")
async def delete_preference(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
    select(UserPreference).where(
        UserPreference.id == preference_id
    )
)
    preference = result.scalar()

    if not preference:
        raise HTTPException(
            status_code=404,
            detail="Preference not found"
        )

    await db.delete(preference)

    await db.commit()

    return {
        "message": "Preference deleted successfully"
    }