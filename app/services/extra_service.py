from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.extra_repository import (
    ExtraRepository
)


class ExtraService:

    @staticmethod
    async def get_extras(
        db: AsyncSession
    ):

        return await ExtraRepository.get_extras(db)


    @staticmethod
    async def select_extra(
        db: AsyncSession,
        cart_id: int,
        extra_id: int
    ):

        return await ExtraRepository.select_extra(
            db,
            cart_id,
            extra_id
        )