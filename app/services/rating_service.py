class RatingService:

    @staticmethod
    async def create_review(db, data):
        return {"status": "review created"}

    @staticmethod
    async def get_order_review(db, order_id):
        return {"order_id": str(order_id), "review": {}}

    @staticmethod
    async def get_driver_reviews(db, driver_id):
        return {"driver_id": str(driver_id), "reviews": []}
