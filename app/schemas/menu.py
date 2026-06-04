from pydantic import BaseModel
from uuid import UUID

class MenuItemOut(BaseModel):
    id: UUID
    restaurant_id: UUID
    item_name: str
    description: str | None = None
    category: str | None = None
    base_price: float
    tags: str | None = None
    tax_rate: str | None = None
    track_stock: bool
    combo_available: bool
    image_url: str | None = None

    class Config:
        from_attributes = True