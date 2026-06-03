from app.core.logger import logger


async def auto_cancel_pending_order(order_id: int, timeout_minutes: int = 10) -> None:
    """Auto-cancel an order if it remains unaccepted past the timeout."""
    logger.info(
        f"[ORDER TASK] Scheduled auto-cancel for order {order_id} "
        f"after {timeout_minutes}m"
    )
    # TODO: implement with Celery or APScheduler


async def update_order_status_on_delivery(order_id: int) -> None:
    """Mark order as delivered after delivery agent confirms."""
    logger.info(f"[ORDER TASK] Marking order {order_id} as delivered")
    # TODO: update Order.status = "delivered" and trigger notification


async def calculate_order_prep_time(order_id: int) -> int:
    """Estimate preparation time based on item count."""
    logger.info(f"[ORDER TASK] Calculating prep time for order {order_id}")
    # TODO: query order items and return estimated minutes
    return 0