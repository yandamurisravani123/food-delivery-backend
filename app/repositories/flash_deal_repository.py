from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.flash_deal import FlashDeal


class FlashDealRepository:

    @staticmethod
    async def get_all(
        session: AsyncSession
    ):

        result = await session.execute(
            select(FlashDeal)
        )

        return result.scalars().all()