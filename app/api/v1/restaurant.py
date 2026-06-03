# app/api/v1/restaurant.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)