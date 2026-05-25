from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.customization_repository import (
    CustomizationRepository
)


class CustomizationService:

    @staticmethod
    async def add_instruction(
        db: AsyncSession,
        item_id: int,
        instruction: str
    ):

        return await CustomizationRepository.add_instruction(
            db,
            item_id,
            instruction
        )