from app.models.delivery_partner_location import (
    DeliveryPartnerLocation
)

from app.models.order_tracking import (
    OrderTracking
)

from app.repositories.tracking_repository import (
    TrackingRepository
)


class TrackingService:

    @staticmethod
    async def get_tracking(
        db,
        order_id
    ):

        return await TrackingRepository.get_tracking(
            db,
            order_id
        )

    @staticmethod
    async def update_location(
        db,
        order_id,
        delivery_partner_id,
        latitude,
        longitude
    ):

        location = DeliveryPartnerLocation(
            order_id=order_id,
            delivery_partner_id=delivery_partner_id,
            latitude=latitude,
            longitude=longitude
        )

        return await TrackingRepository.update_location(
            db,
            location
        )

    @staticmethod
    async def update_status(
        db,
        order_id,
        delivery_partner_id,
        status
    ):

        tracking = OrderTracking(
            order_id=order_id,
            delivery_partner_id=delivery_partner_id,
            status=status
        )

        return await TrackingRepository.update_status(
            db,
            tracking
        )