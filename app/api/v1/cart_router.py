from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db

router = APIRouter(
    prefix="/cart",
    tags=["Add To Cart"]
)

@router.post("/add")
async def add_to_cart(
    food_id: str,
    quantity: int,
    db: AsyncSession = Depends(get_db)
):
    return {
        "message": "Item added to cart"
    }