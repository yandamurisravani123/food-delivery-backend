class MenuService:

    @staticmethod
    async def get_restaurant_menu(db, restaurant_id):
        return {
            "restaurant_id": restaurant_id,
            "menu_items": []
        }
