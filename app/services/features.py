from sqlalchemy.orm import Session
 
from app.models.feature import Feature
 
 
class FeatureService:
 
    @staticmethod
    def get_features_by_plan(
        db: Session,
        plan_id: int
    ):
        return (
            db.query(Feature)
            .filter(
                Feature.plan_id == plan_id
            )
            .all()
        )
 
    @staticmethod
    def create_feature(
        db: Session,
        feature_data
    ):
        feature = Feature(
            plan_id=feature_data.plan_id,
            feature_name=feature_data.feature_name,
            included=feature_data.included
        )
 
        db.add(feature)
        db.commit()
        db.refresh(feature)
 
        return feature
 
    @staticmethod
    def delete_feature(
        db: Session,
        feature_id: int
    ):
        feature = (
            db.query(Feature)
            .filter(
                Feature.id == feature_id
            )
            .first()
        )
 
        if not feature:
            return None
 
        db.delete(feature)
        db.commit()
 
        return {
            "message": "Feature Deleted"
        }