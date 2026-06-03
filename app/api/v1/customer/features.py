from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
 
from app.config.database import get_db
 
from app.schemas.features import (
    FeatureCreate
)

from app.services.features import (
    FeatureService
)
 
router = APIRouter(
    prefix="/features",
    tags=["Features"]
)
 
 
@router.get("/{plan_id}")
def get_plan_features(
    plan_id: int,
    db: Session = Depends(get_db)
):
    return FeatureService.get_features_by_plan(
        db,
        plan_id
    )
 
 
@router.post("/")
def create_feature(
    feature: FeatureCreate,
    db: Session = Depends(get_db)
):
    return FeatureService.create_feature(
        db,
        feature
    )
 
 
@router.delete("/{feature_id}")
def delete_feature(
    feature_id: int,
    db: Session = Depends(get_db)
):
    return FeatureService.delete_feature(
        db,
        feature_id
    )