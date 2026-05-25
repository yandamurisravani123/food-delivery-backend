from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.services.cart_service import (
    CartService
)

router = APIRouter(
    prefix="/cart",
    tags=["Add To Cart"]
)


@router.post("/add")
async def add_to_cart(
    user_id: int,
    food_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db)
):

    cart = await (
        CartService.add_to_cart(
            db,
            user_id,
            food_id,
            quantity
        )
    )

    return {
        "message":
        "Added to cart successfully",
        "data": {
            "cart_id": cart.id,
            "food_id": cart.food_id,
            "quantity": cart.quantity
        }
    }


@router.get("/{user_id}")
async def get_cart(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):

    return await (
        CartService.get_cart(
            db,
            user_id
        )
    )