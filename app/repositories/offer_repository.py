from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.offer import Offer


class OfferRepository:

    @staticmethod
    async def get_all(
        session: AsyncSession
    ):

        result = await session.execute(
            select(Offer)
        )

        return result.scalars().all()