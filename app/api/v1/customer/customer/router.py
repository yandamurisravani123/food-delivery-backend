from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import timezone
from app.config.database import get_db
from app.models.order import Order, OrderItem
from app.models.order import Order, OrderStatus   
from app.schemas.order import OrderCreate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/orders")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):

    
    new_order = Order(
        user_id=order.user_id,
        restaurant_id=order.restaurant_id,
        status=OrderStatus.pending,
        prep_time=len(order.items) * 5  
    )

    db.add(new_order)
    await db.flush()  

    
    for item in order.items:
     db_item = OrderItem(
        order_id=new_order.id,
        name=item.name,
        quantity=item.quantity,
        price=item.price
    )
    db.add(db_item)

    await db.commit()
    await db.refresh(new_order)

    return new_order

@router.get("/")
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    return result.scalars().all()


@router.get("/{order_id}")
async def get_single_order(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await db.delete(order)
    await db.commit()

    return {"message": "Order deleted successfully"}