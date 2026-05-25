from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.cart import Cart
from app.models.user import User
from app.models.food import Food

router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Cart"]
)


@router.post("/add")
async def add_to_cart(
    user_id: int,
    food_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        print("STEP 1")

        user = await db.get(User, user_id)
        print("USER:", user)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        food = await db.get(Food, food_id)
        print("FOOD:", food)

        if not food:
            raise HTTPException(
                status_code=404,
                detail="Food not found"
            )

        cart_item = Cart(
            user_id=user_id,
            food_id=food_id,
            quantity=quantity
        )

        print("STEP 2")

        db.add(cart_item)

        print("STEP 3")

        await db.commit()

        print("STEP 4")

        await db.refresh(cart_item)

        print("STEP 5")

        return {
            "message": "Added to cart successfully",
            "cart_id": cart_item.id
        }

    except Exception as e:
        print("FULL ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )