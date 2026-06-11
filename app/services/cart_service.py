from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.cart_repository import CartRepository


class CartService:

    @staticmethod
    async def add_to_cart(
        db: AsyncSession,
        customer_id: str,
        menu_item_id,
        quantity: int
    ):
        return await CartRepository.add_to_cart(
            db=db,
            customer_id=customer_id,
            menu_item_id=menu_item_id,
            quantity=quantity
        )

    @staticmethod
    async def add_item(
        db: AsyncSession,
        item_id: int,
        quantity: int
    ):
        return await CartRepository.add_item(
            db,
            item_id,
            quantity
        )

    @staticmethod
    async def update_quantity(
        db: AsyncSession,
        cart_id: int,
        quantity: int
    ):
        return await CartRepository.update_quantity(
            db,
            cart_id,
            quantity
        )

    @staticmethod
    async def get_summary(
        db: AsyncSession
    ):
        return await CartRepository.get_summary(db)