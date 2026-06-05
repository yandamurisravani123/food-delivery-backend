from sqlalchemy import select
from app.models.features import Feature


class FeatureService:

    @staticmethod
    async def get_features_by_plan(db, plan_id: int):
        result = await db.execute(
            select(Feature).where(
                Feature.plan_id == plan_id
            )
        )
        return result.scalars().all()

    @staticmethod
    async def create_feature(db, feature_data):
        feature = Feature(**feature_data.model_dump())

        db.add(feature)
        await db.commit()
        await db.refresh(feature)

        return feature

    @staticmethod
    async def delete_feature(db, feature_id: int):
        result = await db.execute(
            select(Feature).where(
                Feature.id == feature_id
            )
        )

        feature = result.scalars().first()

        if not feature:
            return {"message": "Feature not found"}

        await db.delete(feature)
        await db.commit()

        return {"message": "Feature deleted successfully"}