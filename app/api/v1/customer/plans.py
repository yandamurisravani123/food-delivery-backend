from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.core.database import get_db
from app.schemas.plans import (
    PlanCreate,
    PlanResponse,
)
from app.models.plans import Plan
from app.models.features import Feature

router = APIRouter(
    prefix="/plans",
    tags=["Plans"]
)


# ==========================
# GET ALL PLANS
# ==========================
@router.get("/", response_model=List[PlanResponse])
async def get_all_plans(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Plan))
    return result.scalars().all()


# ==========================
# POPULAR PLAN
# ==========================
@router.get("/popular")
async def popular_plan(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Plan).where(Plan.is_popular == True)
    )
    return result.scalars().first()


# ==========================
# ACTIVE PLANS
# ==========================
@router.get("/active")
async def active_plans(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Plan).where(Plan.is_active == True)
    )
    return result.scalars().all()


# ==========================
# SEARCH PLANS
# ==========================
@router.get("/search")
async def search_plans(
    keyword: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Plan).where(
            or_(
                Plan.name.ilike(f"%{keyword}%"),
                Plan.description.ilike(f"%{keyword}%")
            )
        )
    )
    return result.scalars().all()


# ==========================
# PLAN COMPARISON
# ==========================
@router.get("/comparison")
async def plan_comparison(
    db: AsyncSession = Depends(get_db)
):
    plans_result = await db.execute(select(Plan))
    plans = plans_result.scalars().all()

    result = []

    for plan in plans:
        features_result = await db.execute(
            select(Feature).where(
                Feature.plan_id == plan.id
            )
        )

        features = features_result.scalars().all()

        result.append(
            {
                "plan": plan.name,
                "price": plan.price,
                "features": [
                    {
                        "name": feature.feature_name,
                        "included": feature.included
                    }
                    for feature in features
                ]
            }
        )

    return result


# ==========================
# GET PLAN BY ID
# ==========================
@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan_by_id(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Plan).where(Plan.id == plan_id)
    )

    return result.scalars().first()


# ==========================
# CREATE PLAN
# ==========================
@router.post("/")
async def create_plan(
    plan: PlanCreate,
    db: AsyncSession = Depends(get_db)
):
    db_plan = Plan(**plan.model_dump())

    db.add(db_plan)

    await db.commit()
    await db.refresh(db_plan)

    return {
        "id": db_plan.id,
        "created_at": db_plan.created_at,
        "updated_at": db_plan.updated_at,
        "name": db_plan.name
    }


# ==========================
# DELETE PLAN
# ==========================
@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Plan).where(Plan.id == plan_id)
    )

    plan = result.scalars().first()

    if not plan:
        return {"message": "Plan not found"}

    await db.delete(plan)
    await db.commit()

    return {"message": "Plan deleted successfully"}