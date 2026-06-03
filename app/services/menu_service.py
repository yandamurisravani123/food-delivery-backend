from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.menu_repository import MenuRepository


class MenuService:

    @staticmethod
    async def get_restaurant_menu(
        session: AsyncSession,
        restaurant_id
    ):

        menu = await MenuRepository.get_restaurant_menu(
            session,
            restaurant_id
        )

        return {
            "success": True,
            "message": "Menu fetched successfully",
            "data": menu
        }