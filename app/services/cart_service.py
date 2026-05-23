from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException

from app.models.cart import Cart
from app.models.menu import MenuItem


class CartService:

    TAX_PERCENTAGE = 8

    # ADD TO CART
    @staticmethod
    async def add_to_cart(
        db: AsyncSession,
        customer_id,
        menu_item_id,
        quantity: int
    ):

        menu_result = await db.execute(
            select(MenuItem).where(
                MenuItem.id == menu_item_id
            )
        )

        menu_item = (
            menu_result.scalar_one_or_none()
        )

        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail="Menu item not found"
            )

        cart_result = await db.execute(
            select(Cart).where(
                Cart.customer_id == customer_id,
                Cart.menu_item_id == menu_item_id
            )
        )

        cart_item = (
            cart_result.scalar_one_or_none()
        )

        if cart_item:
            cart_item.quantity += quantity

            await db.commit()
            await db.refresh(cart_item)

            return cart_item

        cart_item = Cart(
            customer_id=customer_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            price=menu_item.price
        )

        db.add(cart_item)

        await db.commit()
        await db.refresh(cart_item)

        return cart_item

    # GET CART
    @staticmethod
    async def get_cart(
        db: AsyncSession,
        customer_id
    ):

        result = await db.execute(
            select(Cart).where(
                Cart.customer_id == customer_id
            )
        )

        cart_items = (
            result.scalars().all()
        )

        subtotal = sum(
            item.price * item.quantity
            for item in cart_items
        )

        taxes = (
            subtotal
            * CartService.TAX_PERCENTAGE
        ) / 100

        total = subtotal + taxes

        return {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "delivery_fee": "FREE",
            "taxes": taxes,
            "total": total
        }

    # INCREASE QUANTITY
    @staticmethod
    async def increase_quantity(
        db: AsyncSession,
        cart_id
    ):

        result = await db.execute(
            select(Cart).where(
                Cart.id == cart_id
            )
        )

        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found"
            )

        cart.quantity += 1

        await db.commit()
        await db.refresh(cart)

        return cart

    # DECREASE QUANTITY
    @staticmethod
    async def decrease_quantity(
        db: AsyncSession,
        cart_id
    ):

        result = await db.execute(
            select(Cart).where(
                Cart.id == cart_id
            )
        )

        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found"
            )

        if cart.quantity > 1:
            cart.quantity -= 1

            await db.commit()
            await db.refresh(cart)

        return cart

    # REMOVE ITEM
    @staticmethod
    async def remove_item(
        db: AsyncSession,
        cart_id
    ):

        result = await db.execute(
            select(Cart).where(
                Cart.id == cart_id
            )
        )

        cart = result.scalar_one_or_none()

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found"
            )

        await db.delete(cart)
        await db.commit()

        return {
            "message": "Item removed"
        }