from pydantic import BaseModel
from uuid import UUID


class PreferenceCreate(BaseModel):
    user_id: UUID
    favorite_cuisine: str
    spicy_level: str
    preferred_food_type: str


class PreferenceUpdate(BaseModel):
    favorite_cuisine: str
    spicy_level: str
    preferred_food_type: str


class PreferenceResponse(BaseModel):
    id: UUID          # ✅ Fixed: int -> UUID
    user_id: UUID
    favorite_cuisine: str
    spicy_level: str
    preferred_food_type: str

    class Config:
        from_attributes = True