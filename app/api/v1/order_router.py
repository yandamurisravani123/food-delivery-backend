from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.database import get_db
from app.models.order import Order
from app.models.user import User
from app.schemas.order import (
    OrderCreate,
    OrderResponse
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        # check user exists
        user = await db.get(User, order.user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        new_order = Order(
            user_id=order.user_id,
            food_name=order.food_name,
            cuisine=order.cuisine,
            order_time=order.order_time
        )

        db.add(new_order)

        await db.commit()
        await db.refresh(new_order)

        return new_order

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/", response_model=list[OrderResponse])
async def get_orders(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order)
    )

    orders = result.scalars().all()

    return orders