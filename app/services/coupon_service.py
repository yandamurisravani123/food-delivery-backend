from datetime import datetime, timezone
<<<<<<< HEAD

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.coupon_repository import CouponRepository


class CouponService:

=======
 
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.repositories.coupon_repository import CouponRepository
 
 
class CouponService:
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def create_coupon(
        db: AsyncSession,
        restaurant_id,
        coupon_data,
    ):
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        existing_coupon = await CouponRepository.get_coupon_by_code(
            db,
            coupon_data.coupon_code,
        )
        if existing_coupon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coupon code already exists",
            )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        if coupon_data.start_date >= coupon_data.end_date:
            raise HTTPException(
                status_code=400,
                detail="End date must be greater than start date",
            )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        if coupon_data.discount_type not in ["percentage", "flat"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid discount type",
            )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        coupon_payload = {
            **coupon_data.model_dump(),
            "restaurant_id": restaurant_id,
        }
        return await CouponRepository.create_coupon(
            db,
            coupon_payload,
        )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def validate_coupon(
        db: AsyncSession,
        coupon_code: str,
        order_amount: float,
    ):
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
        coupon = await CouponRepository.get_coupon_by_code(
            db,
            coupon_code,
        )
<<<<<<< HEAD

        if not coupon:
            raise HTTPException(404, "Coupon not found")

        if not coupon.is_active:
            raise HTTPException(400, "Coupon inactive")
        current_time = datetime.now(timezone.utc)

        if current_time < coupon.start_date:
            raise HTTPException(400, "Coupon not started yet")

        if current_time > coupon.end_date:
            raise HTTPException(400, "Coupon expired")

        if coupon.current_usage_count >= coupon.total_usage_limit:
            raise HTTPException(400, "Coupon usage limit exceeded")

=======
 
        if not coupon:
            raise HTTPException(404, "Coupon not found")
 
        if not coupon.is_active:
            raise HTTPException(400, "Coupon inactive")
        current_time = datetime.now(timezone.utc)
 
        if current_time < coupon.start_date:
            raise HTTPException(400, "Coupon not started yet")
 
        if current_time > coupon.end_date:
            raise HTTPException(400, "Coupon expired")
 
        if coupon.current_usage_count >= coupon.total_usage_limit:
            raise HTTPException(400, "Coupon usage limit exceeded")
 
>>>>>>> 6da5f03 (testing)
        if order_amount < coupon.minimum_order_value:
            raise HTTPException(
                400,
                f"Minimum order should be {coupon.minimum_order_value}",
            )
<<<<<<< HEAD

        if coupon.discount_type == "percentage":
            discount = (order_amount * coupon.discount_value) / 100

=======
 
        if coupon.discount_type == "percentage":
            discount = (order_amount * coupon.discount_value) / 100
 
>>>>>>> 6da5f03 (testing)
            if coupon.max_discount_cap:
                discount = min(discount, coupon.max_discount_cap)
        else:
            discount = coupon.discount_value
<<<<<<< HEAD

        final_amount = max(order_amount - discount, 0)

        return {
            "coupon_code": coupon.coupon_code,
            "discount": round(discount, 2),
            "final_amount": round(final_amount, 2)}
=======
 
        final_amount = max(order_amount - discount, 0)
 
        return {
            "coupon_code": coupon.coupon_code,
            "discount": round(discount, 2),
            "final_amount": round(final_amount, 2)}
 
>>>>>>> 6da5f03 (testing)
