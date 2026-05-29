from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from uuid import UUID


# -------------------------
# CREATE
# -------------------------
class GalleryCreate(BaseModel):
    menu_item_id: Optional[UUID] = None
    image_url: HttpUrl


# -------------------------
# ASSIGN
# -------------------------
class GalleryAssign(BaseModel):
    gallery_id: UUID
    menu_item_id: UUID


# -------------------------
# RESPONSE
# -------------------------
class GalleryResponse(BaseModel):
    id: UUID
    restaurant_id: UUID
    menu_item_id: Optional[UUID]
    image_url: HttpUrl
    status: str

    class Config:
        from_attributes = True


# -------------------------
# LIST RESPONSE (optional)
# -------------------------
class GalleryListResponse(BaseModel):
    total: int
    images: List[GalleryResponse]