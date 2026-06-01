from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/api/v1/cart",
    tags=["Add To Cart"]
)


# ADD TO CART
@router.post("/add")
async def add_to_cart(
    food_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {
        "message": "Item added to cart",
        "food_id": food_id,
        "quantity": quantity
    }


# GET ALL CART ITEMS
@router.get("/")
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {"message": "Cart items fetched"}


# UPDATE CART ITEM
@router.patch("/update/{item_id}")
async def update_cart_item(
    item_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {
        "message": "Cart updated",
        "item_id": item_id,
        "quantity": quantity
    }


# REMOVE SINGLE ITEM
@router.delete("/remove/{item_id}")
async def remove_cart_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {
        "message": "Item removed",
        "item_id": item_id
    }


# GET SINGLE CART ITEM
@router.get("/item/{item_id}")
async def get_single_cart_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {
        "message": "Single cart item fetched",
        "item_id": item_id
    }


# CLEAR ENTIRE CART
@router.delete("/clear")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {"message": "Cart cleared successfully"}