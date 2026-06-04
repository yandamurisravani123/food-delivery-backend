class ExtraService:

    @staticmethod
    async def get_extras(db):
        return []

    @staticmethod
    async def select_extra(db, cart_id, extra_id):
        return {
            "cart_id": cart_id,
            "extra_id": extra_id,
            "selected": True
        }
