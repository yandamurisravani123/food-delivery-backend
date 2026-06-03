from pydantic import BaseModel


class BannerResponse(BaseModel):

    id: int

    title: str

    image: str

    class Config:

        from_attributes = True