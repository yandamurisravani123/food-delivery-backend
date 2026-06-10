from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.config.database import get_db
from app.schemas.plans import PlanCreate, PlanUpdate, PlanResponse
from app.services.plans import PlanService
from app.models.plans import Plan
from app.models.features import Feature

router = APIRouter(
    prefix="/plans",
    tags=["Plans"]
)


# ✅ Specific routes BEFORE /{plan_id}
@router.get("/popular")
async def popular_plan(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Plan).where(Plan.is_popular == True)
    )
    return result.scalars().first()


@router.get("/active")
async def active_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Plan).where(Plan.is_active == True)
    )
    return result.scalars().all()


@router.get("/comparison")
async def plan_comparison(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plan))
    plans = result.scalars().all()

    comparison = []
    for plan in plans:
        feat_result = await db.execute(
            select(Feature).where(Feature.plan_id == plan.id)
        )
        features = feat_result.scalars().all()
        comparison.append({
            "plan": plan.name,
            "price": plan.price,
            "features": [
                {"name": f.feature_name, "included": f.included}
                for f in features
            ],
        })
    return comparison


@router.get("/search")
async def search_plans(
    keyword: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Plan).where(
            or_(
                Plan.name.ilike(f"%{keyword}%"),
                Plan.description.ilike(f"%{keyword}%"),
            )
        )
    )
    return result.scalars().all()


# ✅ General routes AFTER specific routes
@router.get("/", response_model=List[PlanResponse])
async def get_all_plans(db: AsyncSession = Depends(get_db)):
    return await PlanService.get_all_plans(db)


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan_by_id(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    plan = await PlanService.get_plan_by_id(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.post("/", response_model=PlanResponse)
async def create_plan(
    plan: PlanCreate,
    db: AsyncSession = Depends(get_db)
):
    return await PlanService.create_plan(db, plan)


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await PlanService.delete_plan(db, plan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Plan not found")
    return result