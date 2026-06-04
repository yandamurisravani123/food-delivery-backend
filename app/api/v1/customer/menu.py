from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.services.menu_service import MenuService

router = APIRouter(
    prefix="/customer/menu",
    tags=["Customer Menu"]
)


@router.get("/{restaurant_id}")
async def get_restaurant_menu(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await MenuService.get_restaurant_menu(
        db,
        restaurant_id
    )