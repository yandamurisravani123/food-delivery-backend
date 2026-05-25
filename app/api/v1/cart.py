from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.cart import Cart
from app.models.food import Food   # change if your menu model name differs
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Add To Cart"]
)


# 1. ADD TO CART
@router.post("/add")
async def add_to_cart(
    food_id: UUID,
    quantity: int = 1,
    customization: str = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # check food exists
    food = await db.execute(
        select(Food).where(Food.id == food_id)
    )
    food_item = food.scalar_one_or_none()

    if not food_item:
        raise HTTPException(
            status_code=404,
            detail="Food item not found"
        )

    cart_item = Cart(
        user_id=current_user.id,
        food_id=food_id,
        quantity=quantity,
        customization=customization
    )

    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)

    return {
        "message": "Item added to cart",
        "cart_id": str(cart_item.id),
        "food_id": str(food_id),
        "quantity": quantity,
        "customization": customization
    }


# 2. GET ALL CART ITEMS
@router.get("/")
async def get_cart_items(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Cart).where(
            Cart.user_id == current_user.id
        )
    )

    cart_items = result.scalars().all()

    return {
        "message": "Cart fetched successfully",
        "items": cart_items
    }


# 3. GET SINGLE CART ITEM
@router.get("/{cart_id}")
async def get_single_cart_item(
    cart_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Cart).where(
            Cart.id == cart_id,
            Cart.user_id == current_user.id
        )
    )

    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    return item


# 4. UPDATE CART ITEM
@router.patch("/update/{cart_id}")
async def update_cart_item(
    cart_id: UUID,
    quantity: int,
    customization: str = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Cart).where(
            Cart.id == cart_id,
            Cart.user_id == current_user.id
        )
    )

    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.quantity = quantity
    cart_item.customization = customization

    await db.commit()
    await db.refresh(cart_item)

    return {
        "message": "Cart updated successfully"
    }


# 5. REMOVE SINGLE ITEM
@router.delete("/remove/{cart_id}")
async def remove_cart_item(
    cart_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Cart).where(
            Cart.id == cart_id,
            Cart.user_id == current_user.id
        )
    )

    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    await db.delete(cart_item)
    await db.commit()

    return {
        "message": "Item removed from cart"
    }


# 6. CLEAR ENTIRE CART
@router.delete("/clear")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    await db.execute(
        delete(Cart).where(
            Cart.user_id == current_user.id
        )
    )

    await db.commit()

    return {
        "message": "Cart cleared successfully"
    }