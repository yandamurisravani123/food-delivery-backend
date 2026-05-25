from pydantic import BaseModel


class PreferenceCreate(BaseModel):
    user_id: int
    favorite_cuisine: str
    spicy_level: str
    preferred_food_type: str


class PreferenceUpdate(BaseModel):
    favorite_cuisine: str
    spicy_level: str
    preferred_food_type: str


class PreferenceResponse(BaseModel):
    id: int
    user_id: int
    favorite_cuisine: str
    spicy_level: str
    preferred_food_type: str

    class Config:
        from_attributes = True