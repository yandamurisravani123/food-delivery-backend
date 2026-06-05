from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu_item import MenuItem


class MenuRepository:

    @staticmethod
    async def get_restaurant_menu(
        session: AsyncSession,
        restaurant_id
    ):
        result = await session.execute(
            select(MenuItem).where(
                MenuItem.restaurant_id == restaurant_id
            )
        )

        return result.scalars().all()