from app.repositories.checkout_repository import (
    CheckoutRepository
)


class CheckoutService:

    @staticmethod
    async def checkout_preview():

        return await CheckoutRepository.checkout_preview()