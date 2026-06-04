from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.cart import Cart
from app.models.menu_item import MenuItem


class CartService:

    @staticmethod
    async def add_to_cart(
        db: AsyncSession,
        customer_id,
        menu_item_id,
        quantity
    ):

        # Check menu item exists
        menu_query = await db.execute(
            select(MenuItem).where(
                MenuItem.id == menu_item_id
            )
        )

        menu_item = menu_query.scalar_one_or_none()

        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail="Menu item not found"
            )

        # Check if already exists in cart
        cart_query = await db.execute(
            select(Cart).where(
                Cart.customer_id == customer_id,
                Cart.menu_item_id == menu_item_id
            )
        )

        existing_item = (
            cart_query.scalar_one_or_none()
        )

        if existing_item:
            existing_item.quantity += quantity

            await db.commit()
            await db.refresh(existing_item)

            return existing_item

        # Add new cart item
        cart_item = Cart(
            customer_id=customer_id,
            menu_item_id=menu_item_id,
            quantity=quantity
        )

        db.add(cart_item)

        await db.commit()
        await db.refresh(cart_item)

        return cart_item