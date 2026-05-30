from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db

from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse
)

from app.services.invoice_service import (
    InvoiceService
)


router = APIRouter(
    prefix="/api/v1/invoice",
    tags=["Invoice"]
)


@router.post(
    "/generate",
    response_model=InvoiceResponse
)
async def generate_invoice(
    payload: InvoiceCreate,
    db: AsyncSession = Depends(get_db)
):

    return await InvoiceService.create_invoice(
        db,
        payload
    )