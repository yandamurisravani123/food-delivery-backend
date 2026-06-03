from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.special_instruction import (
    SpecialInstruction
)


class CustomizationRepository:

    @staticmethod
    async def add_instruction(
        db: AsyncSession,
        item_id: int,
        instruction: str
    ):

        data = SpecialInstruction(
            item_id=item_id,
            instruction=instruction
        )

        db.add(data)

        await db.commit()

        await db.refresh(data)

        return data