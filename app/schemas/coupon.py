from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CouponCreate(BaseModel):
    coupon_code: str = Field(..., min_length=3, max_length=50)

    discount_type: str

    discount_value: float

    max_discount_cap: float | None = None

    minimum_order_value: float = 0

    total_usage_limit: int = 1

    limit_per_customer: int = 1

    start_date: datetime

    end_date: datetime

class CouponUpdate(BaseModel):
    discount_value: float | None = None

    max_discount_cap: float | None = None

    minimum_order_value: float | None = None

    total_usage_limit: int | None = None

    limit_per_customer: int | None = None

    start_date: datetime | None = None

    end_date: datetime | None = None

    is_active: bool | None = None

class CouponOut(BaseModel):
    id: UUID

    restaurant_id: UUID

    coupon_code: str

    discount_type: str

    discount_value: float

    max_discount_cap: float | None

    minimum_order_value: float

    total_usage_limit: int

    current_usage_count: int

    limit_per_customer: int

    start_date: datetime

    end_date: datetime
    is_active: bool

    class Config:
        from_attributes = True