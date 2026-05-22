from pydantic import BaseModel


class MenuItemResponse(BaseModel):

    message: str

    item_id: str