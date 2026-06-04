from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.services.premium_service import (
    PremiumService
)

router = APIRouter(
    prefix="/customer/premium",
    tags=["Premium"]
)


@router.get("/card")
async def get_card(
    user_id: UUID,
    user_name: str,
    db: AsyncSession = Depends(get_db)
):
    return await PremiumService.get_card(
        db,
        user_id,
        user_name
    )


@router.get("/benefits")
async def get_benefits(
    db: AsyncSession = Depends(get_db)
):
    return await PremiumService.get_benefits(db)


@router.get("/status")
async def get_status(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await PremiumService.get_status(
        db,
        user_id
    )


@router.get("/points")
async def get_points(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await PremiumService.get_points(
        db,
        user_id
    )