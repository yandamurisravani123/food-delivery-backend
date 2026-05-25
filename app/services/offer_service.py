from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.offer_repository import (
    OfferRepository
)


class OfferService:

    @staticmethod
    async def get_offers(
        session: AsyncSession
    ):

        offers = await OfferRepository.get_all(
            session
        )

        return {
            "success": True,
            "message": "Offers fetched successfully",
            "data": offers
        }