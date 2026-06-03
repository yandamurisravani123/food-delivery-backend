from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.flash_deal_repository import (
    FlashDealRepository
)


class FlashDealService:

    @staticmethod
    async def get_flash_deals(
        session: AsyncSession
    ):

        deals = await FlashDealRepository.get_all(
            session
        )

        return {
            "success": True,
            "message": "Flash deals fetched successfully",
            "data": deals
        }