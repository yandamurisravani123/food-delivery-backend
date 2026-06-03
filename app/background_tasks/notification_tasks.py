from app.core.logger import logger


async def notify_restaurant_approved(restaurant_id: str) -> None:
    """Notify restaurant owner when their registration is approved."""
    logger.info(f"[NOTIFY] Restaurant {restaurant_id} approved")
    # TODO: push notification or email


async def notify_order_placed(restaurant_id: str, order_id: int) -> None:
    """Notify restaurant of a new incoming order."""
    logger.info(f"[NOTIFY] New order {order_id} for restaurant {restaurant_id}")
    # TODO: push notification or websocket event


async def notify_delivery_agent_assigned(agent_id: str, order_id: int) -> None:
    """Notify delivery agent when they are assigned to an order."""
    logger.info(f"[NOTIFY] Agent {agent_id} assigned to order {order_id}")
    # TODO: push notification


async def notify_customer_order_update(customer_id: str, order_id: int, status: str) -> None:
    """Notify customer about order status change."""
    logger.info(f"[NOTIFY] Order {order_id} status → {status} for customer {customer_id}")
    # TODO: push notification or websocket event