from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.cart import Cart


class CartRepository:

    @staticmethod
    async def add_to_cart(
        db: AsyncSession,
        user_id: int,
        food_id: int,
        quantity: int
    ):

        cart_item = Cart(
            user_id=user_id,
            food_id=food_id,
            quantity=quantity
        )

        db.add(cart_item)

        await db.commit()

        await db.refresh(cart_item)

        return cart_item

    @staticmethod
    async def get_cart(
        db: AsyncSession,
        user_id: int
    ):

        result = await db.execute(
            select(Cart).where(
                Cart.user_id == user_id
            )
        )

        return result.scalars().all()