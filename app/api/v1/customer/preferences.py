from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.preference_schema import (
    SelectPreferenceSchema
)

from app.services.preference_service import (
    PreferenceService
)

router = APIRouter()


@router.get("/menu-items/{item_id}/preferences")
async def get_preferences(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await PreferenceService.get_preferences(db)


@router.post("/cart/select-preference")
async def select_preference(
    payload: SelectPreferenceSchema,
    db: AsyncSession = Depends(get_db)
):

    return await PreferenceService.select_preference(
        db,
        payload.cart_id,
        payload.preference_id
    )


@router.delete("/cart/remove-preference")
async def remove_preference():

    return {
        "message": "Preference removed"
    }