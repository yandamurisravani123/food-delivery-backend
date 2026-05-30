from sqlalchemy import select

from app.models.delivery_partner_location import (
    DeliveryPartnerLocation
)

from app.models.order_tracking import (
    OrderTracking
)


class TrackingRepository:

    @staticmethod
    async def get_tracking(
        db,
        order_id
    ):

        result = await db.execute(
            select(
                DeliveryPartnerLocation
            ).where(
                DeliveryPartnerLocation.order_id == order_id
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def update_location(
        db,
        location
    ):

        db.add(location)

        await db.commit()

        await db.refresh(location)

        return location

    @staticmethod
    async def update_status(
        db,
        tracking
    ):

        db.add(tracking)

        await db.commit()

        await db.refresh(tracking)

        return tracking