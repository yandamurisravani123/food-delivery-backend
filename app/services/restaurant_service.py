from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import hash_password

from app.models import restaurant
from app.repositories.restaurant_repository import (
    RestaurantRepository
)

from app.schemas.restaurant_schema import (
    RestaurantRegisterRequest
)

from app.repositories.menu_repository import (
    MenuRepository
)


from app.utils.email_utils import (
    send_restaurant_approval_email,
    send_restaurant_rejected_email
)


class RestaurantService:


    @staticmethod
    def _serialize_restaurant(restaurant: "restaurant.Restaurant") -> dict:
        return {
            "id": str(restaurant.id),
            "restaurant_name": restaurant.restaurant_name,
            "owner_name": restaurant.owner_name,
            "owner_email": restaurant.owner_email,
            "restaurant_phone": restaurant.restaurant_phone,
            "address_line1": restaurant.address_line1,
            "address_line2": restaurant.address_line2,
            "city": restaurant.city,
            "state": restaurant.state,
            "pincode": restaurant.pincode,
            "latitude": restaurant.latitude,
            "longitude": restaurant.longitude,
            "opening_time": restaurant.opening_time,
            "closing_time": restaurant.closing_time,
            "gst_number": restaurant.gst_number,
            "fssai_number": restaurant.fssai_number,
            "status": restaurant.status,
            "is_active": restaurant.is_active,
            "is_trending": restaurant.is_trending,
            "is_top_rated": restaurant.is_top_rated,
            "cuisine_types": restaurant.cuisine_types,
            "created_at": getattr(restaurant, "created_at", None).isoformat() if getattr(restaurant, "created_at", None) else None,
            "updated_at": getattr(restaurant, "updated_at", None).isoformat() if getattr(restaurant, "updated_at", None) else None,
        }



    # Register Restaurant


    @staticmethod
    async def register_restaurant(
        session: AsyncSession,
        payload: RestaurantRegisterRequest
    ):

        # Check Password Match
        if payload.password != payload.confirm_password:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password do not match"
            )

        # Check Existing Email
        existing = await RestaurantRepository.get_by_owner_email(
            session,
            payload.owner_email
        )

        if existing:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant already registered with this email"
            )

        # Convert Payload
        data = payload.model_dump()

        # Remove confirm password
        data.pop("confirm_password")

        # Hash Password
        data["password_hash"] = hash_password(
            data.pop("password")
        )

        # Default Status
        data["status"] = "pending"

        data["is_active"] = False

       # Create Restaurant
        restaurant = await RestaurantRepository.create_restaurant(
        session,
        data
       )
        return {
            "success": True,
            "message": "Restaurant created successfully",
            "data": RestaurantService._serialize_restaurant(restaurant)
        }

    # Approve Restaurant
  

    @staticmethod
    async def approve_restaurant(
        session: AsyncSession,
        restaurant_id: UUID,
        approved_by: UUID
    ):

        restaurant = await RestaurantRepository.get_by_id(
            session,
            restaurant_id
        )

        if not restaurant:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

        if restaurant.status == "approved":

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant already approved"
            )

        approved_restaurant = await RestaurantRepository.approve_restaurant(
            session,
            restaurant,
            approved_by
        )

        # Send Approval Email
        try:

            send_restaurant_approval_email(
                to_email=approved_restaurant.owner_email,
                restaurant_name=approved_restaurant.restaurant_name
            )

        except Exception:
            pass

        return {
            "success": True,
            "message": "Restaurant approved successfully",
            "data": RestaurantService._serialize_restaurant(approved_restaurant)
        }

   
    # Reject Restaurant
  

    @staticmethod
    async def reject_restaurant(
        session: AsyncSession,
        restaurant_id: UUID,
        approved_by: UUID
    ):

        restaurant = await RestaurantRepository.get_by_id(
            session,
            restaurant_id
        )

        if not restaurant:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

        if restaurant.status == "rejected":

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant already rejected"
            )

        rejected_restaurant = await RestaurantRepository.reject_restaurant(
            session,
            restaurant,
            approved_by
        )

        # Send Rejection Email
        try:

            send_restaurant_rejected_email(
                to_email=rejected_restaurant.owner_email,
                restaurant_name=rejected_restaurant.restaurant_name
            )

        except Exception:
            pass

        return {
            "success": True,
            "message": "Restaurant rejected successfully",
            "data": RestaurantService._serialize_restaurant(rejected_restaurant)
        }

    # Get Pending Restaurants


    @staticmethod
    async def get_pending_restaurants(
        session: AsyncSession
    ):

        restaurants = await RestaurantRepository.list_pending(
            session
        )

        return {
            "success": True,
            "message": "Pending restaurants fetched successfully",
            "data": [RestaurantService._serialize_restaurant(r) for r in restaurants]
        }

    
    # Get All Restaurants


    @staticmethod
    async def get_all(
        session: AsyncSession
    ):

        restaurants = await RestaurantRepository.get_all(
            session
        )

        return {
            "success": True,
            "message": "Restaurants fetched successfully",
            "data": [RestaurantService._serialize_restaurant(r) for r in restaurants]
        }

   
    # Get Restaurant By ID


    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        restaurant_id: UUID
    ):

        restaurant = await RestaurantRepository.get_by_id(
            session,
            restaurant_id
        )

        if not restaurant:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

        return {
            "success": True,
            "message": "Restaurant fetched successfully",
            "data": RestaurantService._serialize_restaurant(restaurant)
        }


    # Nearby Restaurants
  

    @staticmethod
    async def nearby_restaurants(
        session: AsyncSession
    ):

        restaurants = await RestaurantRepository.get_all(
            session
        )

        return {
            "success": True,
            "message": "Nearby restaurants fetched successfully",
            "data": [RestaurantService._serialize_restaurant(r) for r in restaurants]
        }

   

        
    # Restaurant Menu
  

    @staticmethod
    async def restaurant_menu(
        session: AsyncSession,
        restaurant_id: UUID
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

    # Restaurant Reviews


    @staticmethod
    async def restaurant_reviews(
        session: AsyncSession,
        restaurant_id: UUID
    ):

        reviews = await RestaurantRepository.get_restaurant_reviews(
            session,
            restaurant_id
        )
        return {
            "success": True,
            "message": "Restaurant reviews fetched successfully",
            "data": [
                {
                    "id": str(r.id),
                    "restaurant_id": str(r.restaurant_id),
                    "order_id": str(r.order_id),
                    "user_name": r.user_name,
                    "comment": r.comment,
                    "rating": r.rating,
                    "created_at": r.created_at.isoformat() if r.created_at else None
                }
                for r in reviews
            ]
        }