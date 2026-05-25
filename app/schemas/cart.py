from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class AddToCartRequest(BaseModel):
    food_id: UUID
    quantity: int = 1
    customization: Optional[str] = None


class UpdateCartRequest(BaseModel):
    quantity: int