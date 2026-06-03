from uuid import UUID
from pydantic import BaseModel


class RewardPointsResponse(BaseModel):
    current_points: int
    target_points: int


class RewardProgressResponse(BaseModel):
    current_points: int
    target_points: int
    remaining_points: int


class RewardTransactionResponse(BaseModel):
    id: UUID
    points: int
    transaction_type: str
    description: str


class RedeemRewardRequest(BaseModel):
    reward_name: str
    points_required: int


class RedeemRewardResponse(BaseModel):
    message: str


class RewardDashboardResponse(BaseModel):
    current_points: int
    target_points: int
    tier: str