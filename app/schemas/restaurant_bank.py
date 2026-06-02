from pydantic import BaseModel, Field


class RestaurantBankRequest(BaseModel):

    restaurant_id: str

    bank_account_holder: str = Field(...)

    bank_account_number: str = Field(...)

    confirm_account_number: str = Field(...)

    ifsc_code: str = Field(...)