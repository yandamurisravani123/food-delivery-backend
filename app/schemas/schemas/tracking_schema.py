from uuid import UUID

from pydantic import BaseModel


class UpdateLocationRequest(BaseModel):
    latitude: float
    longitude: float


class UpdateStatusRequest(BaseModel):
    status: str


class TrackingResponse(BaseModel):
    order_id: UUID
    latitude: float
    longitude: float
    status: str