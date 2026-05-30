from pydantic import BaseModel
<<<<<<< HEAD


class RevenueReportResponse(BaseModel):

    total_revenue: float

    total_orders: int

    avg_order_value: float

    gst_amount: float

    platform_commission: float

    delivery_fee: float

    net_earnings: float

=======
 
 
class RevenueReportResponse(BaseModel):
 
    total_revenue: float
 
    total_orders: int
 
    avg_order_value: float
 
    gst_amount: float
 
    platform_commission: float
 
    delivery_fee: float
 
    net_earnings: float
 
>>>>>>> 6da5f03 (testing)
    digital_payments: float

    card_payments: float

    cash_on_delivery: float