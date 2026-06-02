from typing import List
 
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
 
from app.config.database import get_db
from app.schemas.plans import (
    PlanCreate,
    PlanUpdate,
    PlanResponse,
)
from app.services.plans import PlanService
from app.models.plans import Plan
from app.models.features import Feature
from sqlalchemy import or_
 
router = APIRouter(
    prefix="/plans",
    tags=["Plans"]
)
 
 
@router.get("/", response_model=List[PlanResponse])
def get_all_plans(
    db: Session = Depends(get_db)
):
    return PlanService.get_all_plans(db)
 
 
@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan_by_id(
    plan_id: int,
    db: Session = Depends(get_db)
):
    return PlanService.get_plan_by_id(
        db,
        plan_id
    )
 
 
@router.post("/", response_model=PlanResponse)
def create_plan(
    plan: PlanCreate,
    db: Session = Depends(get_db)
):
    return PlanService.create_plan(
        db,
        plan
    )
 
 
@router.delete("/{plan_id}")
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    return PlanService.delete_plan(
        db,
        plan_id
    )
@router.get("/popular")
def popular_plan(
    db: Session = Depends(get_db)
):
    return (
        db.query(Plan)
        .filter(Plan.is_popular == True)
        .first()
    )
 
 
@router.get("/active")
def active_plans(
    db: Session = Depends(get_db)
):
    return (
        db.query(Plan)
        .filter(Plan.is_active == True)
        .all()
    )
 
 
@router.get("/comparison")
def plan_comparison(
    db: Session = Depends(get_db)
):
 
    plans = db.query(Plan).all()
 
    result = []
 
    for plan in plans:
 
        features = (
            db.query(Feature)
            .filter(Feature.plan_id == plan.id)
            .all()
        )
 
        result.append(
            {
                "plan": plan.name,
                "price": plan.price,
                "features": [
                    {
                        "name": f.feature_name,
                        "included": f.included,
                    }
                    for f in features
                ],
            }
        )
 
    return result
 
 
@router.get("/search")
def search_plans(
    keyword: str,
    db: Session = Depends(get_db)
):
 
    plans = (
        db.query(Plan)
        .filter(
            or_(
                Plan.name.ilike(f"%{keyword}%"),
                Plan.description.ilike(f"%{keyword}%"),
            )
        )
        .all()
    )
 
    return plans