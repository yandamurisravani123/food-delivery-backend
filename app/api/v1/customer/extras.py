from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.extra_schema import (
    SelectExtraSchema
)

from app.services.extra_service import (
    ExtraService
)

router = APIRouter()


@router.get("/menu-items/{item_id}/extras")
async def get_extras(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await ExtraService.get_extras(db)


@router.post("/cart/select-extra")
async def select_extra(
    payload: SelectExtraSchema,
    db: AsyncSession = Depends(get_db)
):

    return await ExtraService.select_extra(
        db,
        payload.cart_id,
        payload.extra_id
    )


@router.delete("/cart/remove-extra")
async def remove_extra():

    return {
        "message": "Extra removed"
    }