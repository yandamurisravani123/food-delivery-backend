from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cart import Cart


class CartRepository:

    @staticmethod
    async def add_to_cart(
        session: AsyncSession,
        user_id,
        food_id,
        quantity,
        customization
    ):
        cart = Cart(
            user_id=user_id,
            food_id=food_id,
            quantity=quantity,
            customization=customization
        )

        session.add(cart)
        await session.commit()
        await session.refresh(cart)

        return cart

    @staticmethod
    async def get_cart(
        session: AsyncSession,
        user_id
    ):
        result = await session.execute(
            select(Cart).where(
                Cart.user_id == user_id
            )
        )

        return result.scalars().all()

    @staticmethod
    async def update_quantity(
        session: AsyncSession,
        item_id,
        quantity
    ):
        result = await session.execute(
            select(Cart).where(
                Cart.id == item_id
            )
        )

        item = result.scalar_one_or_none()

        if item:
            item.quantity = quantity
            await session.commit()

        return item

    @staticmethod
    async def remove_item(
        session: AsyncSession,
        item_id
    ):
        result = await session.execute(
            select(Cart).where(
                Cart.id == item_id
            )
        )

        item = result.scalar_one_or_none()

        if item:
            await session.delete(item)
            await session.commit()

        return True