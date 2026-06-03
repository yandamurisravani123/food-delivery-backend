# app/schemas/savings.py

from pydantic import BaseModel


class SavingsBreakdown(BaseModel):
    delivery_fee_saved: float
    discount_saved: float
    wallet_credit_saved: float


class TierInfo(BaseModel):
    tier: str
    percentile: float
    next_tier: str
    amount_to_next_tier: float


class SavingsOverview(BaseModel):
    total_saved: float

    breakdown: SavingsBreakdown

    monthly_goal: float
    monthly_saved: float
    progress_percent: float
    remaining_to_goal: float

    tier_info: TierInfo