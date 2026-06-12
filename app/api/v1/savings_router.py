from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db
from app.services.savings_service import SavingsService


router = APIRouter(
    prefix="/savings",
    tags=["Savings"]
)


# --------------------------------
# GET SAVINGS OVERVIEW
# --------------------------------
@router.get("/{user_id}")
async def get_savings_overview(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    overview = await SavingsService.build_overview(
        user_id, db
    )
    return overview