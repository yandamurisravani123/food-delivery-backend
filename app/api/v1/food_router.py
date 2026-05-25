from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.food import Food

from app.schemas.food import (
    FoodCreate,
    FoodUpdate
)


router = APIRouter(
    prefix="/foods",
    tags=["Foods"]
)


# CREATE FOOD
@router.post("/")
async def create_food(
    payload: FoodCreate,
    db: AsyncSession = Depends(get_db)
):

    new_food = Food(
        name=payload.name,
        image=payload.image,
        description=payload.description,
        category=payload.category,
        cuisine=payload.cuisine,
        rating=payload.rating,
        preparation_time=payload.preparation_time,
        tags=payload.tags,
        is_recommended=payload.is_recommended
    )

    db.add(new_food)

    await db.commit()

    await db.refresh(new_food)

    return {
        "message": "Food added successfully",
        "data": new_food
    }


# GET ALL FOODS
@router.get("/")
async def get_all_foods(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Food)
    )

    foods = result.scalars().all()

    return foods


# GET SINGLE FOOD
@router.get("/{food_id}")
async def get_single_food(
    food_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Food).where(
            Food.id == food_id
        )
    )

    food = result.scalar()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return food


# UPDATE FOOD
@router.put("/{food_id}")
async def update_food(
    food_id: int,
    payload: FoodUpdate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Food).where(
            Food.id == food_id
        )
    )

    food = result.scalar()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    food.name = payload.name
    food.image = payload.image
    food.description = payload.description
    food.category = payload.category
    food.cuisine = payload.cuisine
    food.rating = payload.rating
    food.preparation_time = payload.preparation_time
    food.tags = payload.tags
    food.is_recommended = payload.is_recommended

    await db.commit()

    await db.refresh(food)

    return {
        "message": "Food updated successfully",
        "data": food
    }


# DELETE FOOD
@router.delete("/{food_id}")
async def delete_food(
    food_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Food).where(
            Food.id == food_id
        )
    )

    food = result.scalar()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    await db.delete(food)

    await db.commit()

    return {
        "message": "Food deleted successfully"
    }