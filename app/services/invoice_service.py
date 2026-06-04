import random
from fastapi import HTTPException, status
from sqlalchemy import select
 
from app.models.order import Order
from app.repositories.invoice_repository import (
    InvoiceRepository
)
 
 
class InvoiceService:
 
    @staticmethod
    async def create_invoice(db, payload):
 
        result = await db.execute(
            select(Order).where(
                Order.id == payload.order_id
            )
        )

        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
 
        subtotal = 0
 
        for item in payload.items:
 
            subtotal += item.quantity * item.price
 
        gst = subtotal * 0.05
 
        sgst = subtotal * 0.05
 
        total_amount = (
            subtotal
            + payload.delivery_fee
            + gst
            + sgst
        )
 
        invoice_number = str(
            random.randint(10000, 99999)
        )
 
        data = {
 
            "order_id": payload.order_id,
 
            "invoice_number": invoice_number,
 
            "restaurant_name": payload.restaurant_name,
 
            "restaurant_gstin": payload.restaurant_gstin,
 
            "customer_gstin": payload.customer_gstin,
 
            "subtotal": subtotal,
 
            "delivery_fee": payload.delivery_fee,
 
            "gst": gst,
 
            "sgst": sgst,
 
            "total_amount": total_amount
        }
 
        invoice = await InvoiceRepository.create_invoice(
            db,
            data,
            payload.items
        )
 
        return {
 
            "invoice_id": str(invoice.id),
 
            "invoice_number": invoice.invoice_number,
 
            "total_amount": invoice.total_amount,
 
            "message": "Invoice Generated Successfully"
        }
 