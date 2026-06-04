from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.security import hash_password
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant import RestaurantRegisterRequest
from app.models.restaurant import Restaurant
from app.utils.email_utils import send_restaurant_approval_email, send_restaurant_rejected_email
from app.services.menu_service import MenuService
from app.services.review_service import ReviewService

class RestaurantService:
    @staticmethod
    async def register_restaurant(session: AsyncSession, payload: RestaurantRegisterRequest):
        if payload.password != payload.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password do not match",
            )

        existing = await RestaurantRepository.get_by_owner_email(session, payload.owner_email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant already registered with this email",
            )

        data = payload.model_dump()
        data.pop("confirm_password")
        data["password_hash"] = hash_password(data.pop("password"))
        data["status"] = "pending"
        data["is_active"] = False

        restaurant = await RestaurantRepository.create_restaurant(session, data)
        return restaurant

    @staticmethod
    async def approve_restaurant(session, restaurant_id, approved_by):
        restaurant = await RestaurantRepository.get_by_id(session, restaurant_id)

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        if restaurant.status == "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant already approved",
            )

        approved_restaurant = await RestaurantRepository.approve_restaurant(
            session, restaurant, approved_by
        )

        try:
            send_restaurant_approval_email(
                to_email=approved_restaurant.owner_email,
                restaurant_name=approved_restaurant.restaurant_name,
            )
        except Exception:
            pass

        return approved_restaurant

    @staticmethod
    async def reject_restaurant(session, restaurant_id, approved_by):
        restaurant = await RestaurantRepository.get_by_id(session, restaurant_id)

        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )

        if restaurant.status == "rejected":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant already rejected",
            )

        rejected_restaurant = await RestaurantRepository.reject_restaurant(
            session, restaurant, approved_by
        )

        try:
            send_restaurant_rejected_email(
                to_email=rejected_restaurant.owner_email,
                restaurant_name=rejected_restaurant.restaurant_name,
            )
        except Exception:
            pass

        return rejected_restaurant

    @staticmethod
    async def get_pending_restaurants(session: AsyncSession):
        return await RestaurantRepository.list_pending(session)
    
    @staticmethod
    async def get_all(session):
        return await RestaurantRepository.get_all(session)

    @staticmethod
    async def get_by_id(session, restaurant_id):
        restaurant = await RestaurantRepository.get_by_id(session, restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        return restaurant

    @staticmethod
    async def nearby_restaurants(session: AsyncSession):
        # Return active restaurants; fallback to all restaurants
        try:
            restaurants = await RestaurantRepository.get_all(session)
        except Exception:
            restaurants = []
        return restaurants

    @staticmethod
    async def restaurant_menu(session: AsyncSession, restaurant_id):
        # Delegate to MenuService (stubbed)
        return await MenuService.get_restaurant_menu(session, restaurant_id)

    @staticmethod
    async def restaurant_reviews(session: AsyncSession, restaurant_id):
        # Use ReviewService if available; otherwise return empty list
        try:
            # ReviewService does not have a dedicated restaurant method yet
            return []
        except Exception:
            return []