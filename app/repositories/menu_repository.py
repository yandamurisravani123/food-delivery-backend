from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import Menu


class MenuRepository:

    @staticmethod
    async def get_restaurant_menu(
        session: AsyncSession,
        restaurant_id
    ):
        result = await session.execute(
            select(Menu).where(
                Menu.restaurant_id == restaurant_id
            )
        )

        return result.scalars().all()