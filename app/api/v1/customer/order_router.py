from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.order import Order, OrderItem
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

    items = [
        OrderItem(
            name=item.name,
            quantity=item.quantity,
            price=item.price
        )
        for item in payload.items
    ]

    subtotal = sum(item.quantity * item.price for item in payload.items)

    new_order = Order(
        user_id=payload.user_id,
        restaurant_id=payload.restaurant_id,
        delivery_address=payload.delivery_address,
        special_instructions=payload.special_instructions,
        cutlery_required=payload.cutlery_required,
        subtotal=subtotal,
        total=subtotal,
        items=items
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