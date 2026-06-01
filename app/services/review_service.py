import uuid

from app.models.review import Review

from app.repositories.review_repository import (
    ReviewRepository
)

from app.utils.file_upload import (
    save_file
)


class ReviewService:

    
    # 1. GET ORDER DETAILS
    

    @staticmethod
    async def get_order_details(
        db,
        order_id
    ):

        return {
            "order_id": str(order_id),
            "name": "Restaurant"
        }

    
    # 2. SUBMIT REVIEW


    @staticmethod
    async def submit_restaurant_review(
        db,
        request
    ):

        review = Review(
            id=uuid.uuid4(),
            order_id=request.order_id,
            restaurant_id=request.restaurant_id,
            user_name=request.user_name,
            comment=request.comment,
            rating=request.rating
        )

        review = await ReviewRepository.create_review(
            db,
            review
        )

        return {
            "success": True,
            "message": "Review submitted successfully",
            "review_id": str(review.id)
        }

    
    # 3. UPLOAD REVIEW PHOTOS
    
    @staticmethod
    async def upload_review_photos(
        db,
        order_id,
        photos
    ):

        uploaded_photos = []

        for photo in photos:

            file_path = await save_file(
                photo
            )

            uploaded_photos.append({
                "photo_name": photo.filename,
                "photo_url": file_path
            })

        return {
            "success": True,
            "photos": uploaded_photos
        }

    
    # 4. DELETE PHOTO
   

    @staticmethod
    async def delete_review_photo(
        db,
        photo_id
    ):

        return {
            "success": True,
            "message": "Photo deleted successfully"
        }


    # 5. DELIVERY FEEDBACK


    @staticmethod
    async def get_delivery_feedback(
        db,
        order_id
    ):

        return {
            "order_id": str(order_id),
            "message": "Delivery feedback screen"
        }

    
    # 6. REVIEW STATUS
    
    @staticmethod
    async def check_review_status(
        db,
        order_id
    ):

        review = await ReviewRepository.get_review_by_order(
            db,
            order_id
        )

        return {
            "already_reviewed": review is not None
        }