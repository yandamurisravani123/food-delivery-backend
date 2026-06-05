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

        grouped_menu = {}

        for item in menu:

            category = item.category or "Others"

            if category not in grouped_menu:
                grouped_menu[category] = []

            grouped_menu[category].append({
                "id": str(item.id),
                "item_name": item.item_name,
                "price": item.base_price,
                "available": item.is_available,
                "image": item.image_url
            })

        return {
    "success": True,
    "message": "Restaurant menu fetched successfully",
    "count": len(menu),
    "data": grouped_menu
}