from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.extra import Extra
from app.models.cart_extra import CartExtra


class ExtraRepository:

    @staticmethod
    async def get_extras(
        db: AsyncSession
    ):

        result = await db.execute(
            select(Extra)
        )

        return result.scalars().all()


    @staticmethod
    async def select_extra(
        db: AsyncSession,
        cart_id: int,
        extra_id: int
    ):

        data = CartExtra(
            cart_id=cart_id,
            extra_id=extra_id
        )

        db.add(data)

        await db.commit()

        return data


    @staticmethod
    async def remove_extra(
        db: AsyncSession
    ):

        return {
            "message": "Extra removed"
        }