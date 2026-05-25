from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cart import Cart


class CartRepository:

    @staticmethod
    async def add_item(
        db: AsyncSession,
        item_id: int,
        quantity: int
    ):

        cart = Cart(
            item_id=item_id,
            quantity=quantity,
            total_price=25.0
        )

        db.add(cart)

        await db.commit()

        await db.refresh(cart)

        return cart


    @staticmethod
    async def update_quantity(
        db: AsyncSession,
        cart_id: int,
        quantity: int
    ):

        result = await db.execute(
            select(Cart).where(
                Cart.id == cart_id
            )
        )

        cart = result.scalar_one_or_none()

        if cart:
            cart.quantity = quantity

            await db.commit()

            await db.refresh(cart)

        return cart


    @staticmethod
    async def get_summary(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Cart)
        )

        return result.scalars().all()