from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.preference_repository import (
    PreferenceRepository
)


class PreferenceService:

    @staticmethod
    async def get_preferences(
        db: AsyncSession
    ):

        return await PreferenceRepository.get_preferences(db)


    @staticmethod
    async def select_preference(
        db: AsyncSession,
        cart_id: int,
        preference_id: int
    ):

        return await PreferenceRepository.select_preference(
            db,
            cart_id,
            preference_id
        )