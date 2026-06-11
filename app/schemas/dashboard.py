from pydantic import BaseModel


class OperationsDashboardResponse(BaseModel):
    total_orders: int
    completed_orders: int
    cancelled_orders: int
    active_drivers: int
    active_restaurants: int


class KPIDashboardResponse(BaseModel):
    total_revenue: float
    average_order_value: float
    customer_retention_rate: float
    delivery_success_rate: float


class LiveOrderResponse(BaseModel):
    order_id: int
    customer_name: str
    restaurant_name: str
    driver_name: str | None
    status: str
    amount: float