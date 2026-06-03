# OrderItem is defined in order.py alongside the Order model.
# This file re-exports it for compatibility with imports that use order_items module.
from app.models.order import OrderItem

__all__ = ["OrderItem"]
