from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# CREATE ORDER
@router.post("/")
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db)
):

    new_order = Order(
        user_id=payload.user_id,
        food_name=payload.food_name,
        cuisine=payload.cuisine,
        order_time=payload.order_time
    )

    db.add(new_order)

    await db.commit()

    await db.refresh(new_order)

    return {
        "message": "Order created successfully",
        "data": new_order
    }


# GET ALL ORDERS
@router.get("/")
async def get_orders(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order)
    )

    orders = result.scalars().all()

    return orders


# GET SINGLE ORDER
@router.get("/{order_id}")
async def get_single_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order).where(
            Order.id == order_id
        )
    )

    order = result.scalar()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# DELETE ORDER
@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order).where(
            Order.id == order_id
        )
    )

    order = result.scalar()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    await db.delete(order)

    await db.commit()

    return {
        "message": "Order deleted successfully"
    }