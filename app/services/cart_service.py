from app.repositories.cart_repository import (
    CartRepository
)


class CartService:

    @staticmethod
    async def add_to_cart(
        db,
        user_id,
        food_id,
        quantity
    ):
        return await (
            CartRepository.add_to_cart(
                db,
                user_id,
                food_id,
                quantity
            )
        )

    @staticmethod
    async def get_cart(
        db,
        user_id
    ):
        return await (
            CartRepository.get_cart(
                db,
                user_id
            )
        )