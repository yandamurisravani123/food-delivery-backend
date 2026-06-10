from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.config.database import get_db
from app.models.cart import Cart
from app.models.food import Food

router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"]
)


@router.post("/add")
async def add_to_cart(
    food_id: int,
    quantity: int,
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Food).where(Food.id == food_id)
    )
    food = result.scalar_one_or_none()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    cart_item = Cart(
        customer_id=user_id,
        food_id=food_id,
        quantity=quantity,
        total_price=food.price * quantity
    )

    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)

    return {
        "success": True,
        "message": "Added to cart successfully"
    }