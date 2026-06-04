from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.delivery_notification import (
    DeliveryNotification
)
from app.models.order import Order


router = APIRouter(
    prefix="/delivery-notifications",
    tags=["Delivery Notifications"]
)


# --------------------------------
# CREATE DELIVERY NOTIFICATION
# --------------------------------
@router.post("/create")
async def create_notification(
    user_id: int,
    order_id: int,
    title: str,
    message: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order).where(
            Order.id == order_id
        )
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    notification = DeliveryNotification(
        user_id=user_id,
        order_id=order_id,
        title=title,
        message=message
    )

    db.add(notification)

    await db.commit()

    await db.refresh(notification)

    return {
        "message":
        "Notification created",
        "data": notification
    }


# --------------------------------
# GET USER NOTIFICATIONS
# --------------------------------
@router.get("/{user_id}")
async def get_notifications(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(DeliveryNotification)
        .where(
            DeliveryNotification.user_id
            == user_id
        )
    )

    notifications = (
        result.scalars().all()
    )

    return {
        "notifications":
        notifications
    }


# --------------------------------
# MARK AS READ
# --------------------------------
@router.patch("/read/{notification_id}")
async def mark_as_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(DeliveryNotification)
        .where(
            DeliveryNotification.id
            == notification_id
        )
    )

    notification = (
        result.scalar_one_or_none()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    await db.commit()

    return {
        "message":
        "Notification marked as read"
    }


# --------------------------------
# DELETE NOTIFICATION
# --------------------------------
@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(DeliveryNotification)
        .where(
            DeliveryNotification.id
            == notification_id
        )
    )

    notification = (
        result.scalar_one_or_none()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    await db.delete(notification)

    await db.commit()

    return {
        "message":
        "Notification deleted"
    }