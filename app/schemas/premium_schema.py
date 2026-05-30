from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class PremiumCardResponse(BaseModel):
    member_code: str
    member_name: str
    member_since: datetime
    qr_code: str


class MembershipStatusResponse(BaseModel):
    is_active: bool
    plan_name: str
    next_billing_date: datetime


class BenefitResponse(BaseModel):
    title: str
    description: str


class RewardPointResponse(BaseModel):
    current_points: int
    target_points: int