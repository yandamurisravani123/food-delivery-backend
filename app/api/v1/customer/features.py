from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.features import FeatureCreate
from app.services.features import FeatureService

router = APIRouter(
    prefix="/features",
    tags=["Features"]
)


@router.get("/{plan_id}")
async def get_plan_features(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await FeatureService.get_features_by_plan(db, plan_id)


@router.post("/")
async def create_feature(
    feature: FeatureCreate,
    db: AsyncSession = Depends(get_db)
):
    return await FeatureService.create_feature(db, feature)


@router.delete("/{feature_id}")
async def delete_feature(
    feature_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await FeatureService.delete_feature(db, feature_id)
    if not result:
        raise HTTPException(status_code=404, detail="Feature not found")
    return result