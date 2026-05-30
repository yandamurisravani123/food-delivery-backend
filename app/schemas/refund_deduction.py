from pydantic import BaseModel
from typing import List
 
 
class RefundDeductionItem(BaseModel):
 
    order_id: str
 
    category: str
 
    reason: str
 
    deduction_amount: float
 
    refund_status: str
 
    risk_level: str
 
    created_at_label: str
 
    class Config:
 
        from_attributes = True
 
 
class RefundDeductionResponse(BaseModel):
 
    total_deductions: float
 
    customer_refunds: float
 
    penalty_fees: float
 
    dispute_success_rate: float
 
    total_active_cases: int
 
    total_pending_cases: int
 
    deductions: List[RefundDeductionItem]
 