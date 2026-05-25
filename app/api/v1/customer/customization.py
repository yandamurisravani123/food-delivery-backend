from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.customization_schema import (
    SpecialInstructionSchema
)

from app.services.customization_service import (
    CustomizationService
)

router = APIRouter()


@router.get("/menu-items/{item_id}/customization")
async def get_customization(
    item_id: int
):

    return {
        "item_id": item_id,
        "message": "Customization details"
    }


@router.post("/menu-items/{item_id}/special-instructions")
async def add_instruction(
    item_id: int,
    payload: SpecialInstructionSchema,
    db: AsyncSession = Depends(get_db)
):

    return await CustomizationService.add_instruction(
        db,
        item_id,
        payload.instruction
    )