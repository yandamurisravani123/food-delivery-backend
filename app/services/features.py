from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.features import Feature


class FeatureService:

    @staticmethod
    async def get_features_by_plan(db: AsyncSession, plan_id: int):
        result = await db.execute(
            select(Feature).where(Feature.plan_id == plan_id)
        )
        return result.scalars().all()

    @staticmethod
    async def create_feature(db: AsyncSession, feature_data):
        feature = Feature(
            plan_id=feature_data.plan_id,
            feature_name=feature_data.feature_name,
            included=feature_data.included,
        )
        db.add(feature)
        await db.commit()
        await db.refresh(feature)
        return feature

    @staticmethod
    async def delete_feature(db: AsyncSession, feature_id: int):
        result = await db.execute(
            select(Feature).where(Feature.id == feature_id)
        )
        feature = result.scalar_one_or_none()

        if not feature:
            return None

        await db.delete(feature)
        await db.commit()

        return {"message": "Feature deleted"}