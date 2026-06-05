from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.models.cuisine import Cuisine
from app.services.cuisine_service import CuisineService

router = APIRouter(
    prefix="/customer/cuisine",
    tags=["Cuisine"]
)


# CREATE CUISINE
@router.post("/")
async def create_cuisine(
    name: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    cuisine = Cuisine(
        name=name,
        image=image.filename
    )

    db.add(cuisine)

    await db.commit()

    await db.refresh(cuisine)

    return {
        "success": True,
        "message": "Cuisine created successfully",
        "data": {
            "id": cuisine.id,
            "name": cuisine.name,
            "image": cuisine.image
        }
    }


# GET ALL CUISINES
@router.get("/")
async def get_cuisines(
    db: AsyncSession = Depends(get_db)
):

    cuisines = await CuisineService.get_cuisines(db)

    return {
        "success": True,
        "count": len(cuisines),
        "data": [
            {
                "id": cuisine.id,
                "name": cuisine.name,
                "image": cuisine.image
            }
            for cuisine in cuisines
        ]
    }