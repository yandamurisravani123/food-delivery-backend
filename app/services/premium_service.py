class PremiumService:

    @staticmethod
    async def get_card(db, user_id, user_name):
        return {
            "user_id": str(user_id),
            "user_name": user_name,
            "card_status": "active"
        }

    @staticmethod
    async def get_benefits(db):
        return [
            {"benefit": "Free delivery"},
            {"benefit": "Priority support"}
        ]

    @staticmethod
    async def get_status(db, user_id):
        return {
            "user_id": str(user_id),
            "status": "active"
        }

    @staticmethod
    async def get_points(db, user_id):
        return {
            "user_id": str(user_id),
            "points": 100
        }
