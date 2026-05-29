from pydantic import BaseModel
from typing import List


class TaxInvoiceItem(BaseModel):

    invoice_id: str

    month: str

    invoice_type: str

    gst_amount: float

    tds_amount: float

    total_amount: float

    class Config:

        from_attributes = True


class TaxInvoiceListResponse(BaseModel):

    financial_year: str

    total_tds_withheld: float

    net_gst_claimable: float

    invoice_count: int

    invoices: List[TaxInvoiceItem]


class TaxSummaryResponse(BaseModel):

    message: str