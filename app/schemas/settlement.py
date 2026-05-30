 
from pydantic import BaseModel
from typing import List
 
 
class SettlementItem(BaseModel):
 
    settlement_id: str
 
    cycle: str
 
    gross_sales: float
 
    deductions: float
 
    net_payout: float
 
    platform_fees: float
 
    discounts: float
 
    tax_adjustment: float
 
    merchant_share_percentage: float
 
    platform_fee_percentage: float
 
    discount_percentage: float
 
    # NEW
    merchant_share: float
 
    # NEW
    delivery_commission: float
 
    # NEW
    payment_gateway_fee: float
 
    # NEW
    total_orders: int
 
    status: str
 
    class Config:
 
        from_attributes = True
 
 
class RevenueSplit(BaseModel):
 
    merchant_share: float
 
    platform_fees: float
 
    discounts: float
 
    merchant_share_percentage: float
 
    platform_fee_percentage: float
 
    discount_percentage: float
 
 
class ServiceFeeItem(BaseModel):
 
    service_name: str
 
    amount: float
 
 
class SettlementDetailsResponse(BaseModel):
 
    settlement: SettlementItem
 
    revenue_split: RevenueSplit
 
    service_fees: List[ServiceFeeItem]
 
 
class SettlementResponse(BaseModel):
 
    current_period_amount: float
 
    next_payout_amount: float
 
    processing_percentage: int
 
    estimated_date: str
 
    settlements: List[SettlementItem]
 
 