from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.cart_schema import (
    AddCustomizedItemSchema,
    UpdateQuantitySchema
)

from app.services.cart_service import (
    CartService
)

router = APIRouter()


@router.post("/cart/add-customized-item")
async def add_customized_item(
    payload: AddCustomizedItemSchema,
    db: AsyncSession = Depends(get_db)
):

    return await CartService.add_item(
        db,
        payload.item_id,
        payload.quantity
    )


@router.put("/cart/update-item-quantity")
async def update_item_quantity(
    payload: UpdateQuantitySchema,
    db: AsyncSession = Depends(get_db)
):

    return await CartService.update_quantity(
        db,
        payload.cart_id,
        payload.quantity
    )


@router.get("/cart/summary")
async def cart_summary(
    db: AsyncSession = Depends(get_db)
):

    return await CartService.get_summary(db)