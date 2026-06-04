class ReviewService:

    @staticmethod
    async def get_order_details(db, order_id):
        return {"order_id": order_id, "details": {}}

    @staticmethod
    async def submit_restaurant_review(db, request):
        return {"status": "review submitted"}

    @staticmethod
    async def upload_review_photos(db, order_id, photos):
        return {"order_id": order_id, "uploaded": len(photos)}

    @staticmethod
    async def delete_review_photo(db, photo_id):
        return {"photo_id": photo_id, "deleted": True}

    @staticmethod
    async def get_delivery_feedback(db, order_id):
        return {"order_id": order_id, "feedback": []}

    @staticmethod
    async def check_review_status(db, order_id):
        return {"order_id": order_id, "status": "pending"}
