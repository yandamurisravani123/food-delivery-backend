import random
 
from app.models.invoice import Invoice
 
from app.models.invoice_item import InvoiceItem
 
 
class InvoiceRepository:
 
    @staticmethod
    async def create_invoice(db, data, items):
 
        invoice = Invoice(**data)
 
        db.add(invoice)
 
        await db.flush()
 
        for item in items:
 
            total = item.quantity * item.price
 
            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                item_name=item.item_name,
                description=item.description,
                quantity=item.quantity,
                price=item.price,
                total=total
            )
 
            db.add(invoice_item)
 
        await db.commit()
 
        await db.refresh(invoice)
 
        return invoice
 