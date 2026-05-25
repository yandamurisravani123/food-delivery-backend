from pydantic import BaseModel


class FoodCreate(BaseModel):
    name: str
    image: str
    description: str
    category: str
    cuisine: str
    rating: float
    preparation_time: str
    tags: str
    is_recommended: bool


class FoodUpdate(BaseModel):
    name: str
    image: str
    description: str
    category: str
    cuisine: str
    rating: float
    preparation_time: str
    tags: str
    is_recommended: bool


class FoodResponse(BaseModel):
    id: int
    name: str
    image: str
    description: str
    category: str
    cuisine: str
    rating: float
    preparation_time: str
    tags: str
    is_recommended: bool

    class Config:
        from_attributes = True