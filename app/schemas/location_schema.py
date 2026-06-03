from pydantic import BaseModel


class LocationResponse(BaseModel):

    id: int

    city: str

    state: str

    class Config:

        from_attributes = True