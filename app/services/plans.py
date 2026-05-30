from sqlalchemy.orm import Session
from app.models.plan import Plan
 
 
class PlanService:
 
    @staticmethod
    def get_all_plans(db: Session):
        return db.query(Plan).all()
 
    @staticmethod
    def get_plan_by_id(
        db: Session,
        plan_id: int
    ):
        return (
            db.query(Plan)
            .filter(Plan.id == plan_id)
            .first()
        )
 
    @staticmethod
    def create_plan(
        db: Session,
        plan_data
    ):
        plan = Plan(
            name=plan_data.name,
            price=plan_data.price,
            description=plan_data.description,
            duration_days=plan_data.duration_days,
            free_trial_days=plan_data.free_trial_days,
            is_popular=plan_data.is_popular
        )
 
        db.add(plan)
        db.commit()
        db.refresh(plan)
 
        return plan
 
    @staticmethod
    def delete_plan(
        db: Session,
        plan_id: int
    ):
        plan = (
            db.query(Plan)
            .filter(Plan.id == plan_id)
            .first()
        )
 
        if not plan:
            return None
 
        db.delete(plan)
        db.commit()
 
        return {
            "message": "Plan Deleted"
        }