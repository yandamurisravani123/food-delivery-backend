from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.coupon import Coupon
<<<<<<< HEAD

class CouponRepository:

    @staticmethod
    async def create_coupon(db: AsyncSession, coupon_data: dict):
        coupon = Coupon(**coupon_data)

        db.add(coupon)

        await db.commit()

        await db.refresh(coupon)

        return coupon
    
=======
 
class CouponRepository:
 
    @staticmethod
    async def create_coupon(db: AsyncSession, coupon_data: dict):
        coupon = Coupon(**coupon_data)
 
        db.add(coupon)
 
        await db.commit()
 
        await db.refresh(coupon)
 
        return coupon
   
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_coupon_by_code(
        db: AsyncSession,
        coupon_code: str,
    ):
        query = select(Coupon).where(
            Coupon.coupon_code == coupon_code
        )
<<<<<<< HEAD

        result = await db.execute(query)

        return result.scalar_one_or_none()


=======
 
        result = await db.execute(query)
 
        return result.scalar_one_or_none()
 
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_restaurant_coupons(
        db: AsyncSession,
        restaurant_id: UUID,
    ):
        query = select(Coupon).where(
            Coupon.restaurant_id == restaurant_id
        )
<<<<<<< HEAD

        result = await db.execute(query)
        return result.scalars().all()


=======
 
        result = await db.execute(query)
        return result.scalars().all()
 
 
>>>>>>> 6da5f03 (testing)
    @staticmethod
    async def get_coupon_by_id(
        db: AsyncSession,
        coupon_id: UUID,
    ):
        query = select(Coupon).where(Coupon.id == coupon_id)
<<<<<<< HEAD

        result = await db.execute(query)

        return result.scalar_one_or_none()


    @staticmethod
    async def delete_coupon(db: AsyncSession, coupon: Coupon):
        await db.delete(coupon)

        await db.commit()
=======
 
        result = await db.execute(query)
 
        return result.scalar_one_or_none()
 
 
    @staticmethod
    async def delete_coupon(db: AsyncSession, coupon: Coupon):
        await db.delete(coupon)
 
        await db.commit()
 
>>>>>>> 6da5f03 (testing)
