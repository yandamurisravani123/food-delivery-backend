# app/services/order_tracking_service.py

from app.repositories.order_tracking_repository import (
    OrderTrackingRepository
)


class OrderTrackingService:

    @staticmethod
    async def get_tracking(
        db,
        order_id
    ):
        return await (
            OrderTrackingRepository
            .get_order_tracking(
                db,
                order_id
            )
        )

    @staticmethod
    async def update_location(
        db,
        order_id,
        latitude,
        longitude
    ):
        return await (
            OrderTrackingRepository
            .update_driver_location(
                db,
                order_id,
                latitude,
                longitude
            )
        )