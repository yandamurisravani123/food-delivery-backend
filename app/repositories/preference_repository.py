from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.preference import Preference
from app.models.cart_preference import (
    CartPreference
)


class PreferenceRepository:

    @staticmethod
    async def get_preferences(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Preference)
        )

        return result.scalars().all()


    @staticmethod
    async def select_preference(
        db: AsyncSession,
        cart_id: int,
        preference_id: int
    ):

        data = CartPreference(
            cart_id=cart_id,
            preference_id=preference_id
        )

        db.add(data)

        await db.commit()

        return data