class PreferenceService:

    @staticmethod
    async def get_preferences(db):
        return []

    @staticmethod
    async def select_preference(db, cart_id, preference_id):
        return {
            "cart_id": cart_id,
            "preference_id": preference_id,
            "selected": True
        }
