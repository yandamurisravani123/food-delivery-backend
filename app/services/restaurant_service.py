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

        return restaurant

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
            "data": approved_restaurant
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
            "data": rejected_restaurant
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
            "data": restaurants
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
            "data": restaurants
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
            "data": restaurant
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
            "data": restaurants
        }

    # Restaurant Menu
   

        # ==========================================
    # Restaurant Menu
    # ==========================================

    @staticmethod
    async def restaurant_menu(
        session: AsyncSession,
        restaurant_id: UUID
    ):

        menu = await MenuRepository.get_restaurant_menu(
            session,
            restaurant_id
        )

        return {
            "success": True,
            "message": "Restaurant menu fetched successfully",
            "data": menu
        }

    # ==========================================
    # Restaurant Reviews
    # ==========================================

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
            "data": reviews
        }