from app.repositories.cart_repository import CartRepository


class CartService:

    @staticmethod
    async def add_to_cart(
        session,
        user_id,
        payload
    ):
        return await CartRepository.add_to_cart(
            session=session,
            user_id=user_id,
            food_id=payload.food_id,
            quantity=payload.quantity,
            customization=payload.customization
        )

    @staticmethod
    async def get_cart(
        session,
        user_id
    ):
        return await CartRepository.get_cart(
            session,
            user_id
        )