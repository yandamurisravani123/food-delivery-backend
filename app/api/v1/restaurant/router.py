from celery import app
from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast, String
from uuid import UUID
import pandas as pd
from typing import List, Optional
from fastapi import UploadFile, File, Form, Query
import os
import shutil
import uuid
from sqlalchemy.orm import Session, selectinload
from app.config.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models import menu, order, user         
from app.schemas import order
from app.schemas.menu import MenuItemOut
from app.schemas.restaurant_bank import RestaurantBankRequest
from app.models.combo import MealCombo
from app.models.customization import (
    CustomizationGroup,
    CustomizationOption
)

from app.models.pricing_rule import PricingRule
from app.models.pricing_analytics import PricingAnalytics
from app.models.menu_schedule import MenuSchedule

from app.models.gallery import Gallery

from app.models.order import Order, OrderStatus
from app.models.order_items import OrderItem
from sqlalchemy import func,select
from datetime import datetime, timedelta, timezone
from app.models.user import User

from app.services.analytics_service import (

    get_top_selling_by_quantity,

    get_top_selling_by_revenue,

    get_category_insights,
 
    get_menu_rankings,
 
    get_dashboard_data
)

from app.services.dashboard_service import DashboardService
from app.services.campaign_service import DashboardService as CampaignDashboardService
from app.schemas.dashboard import DashboardSummaryResponse
from app.models.revenue_report import RevenueReport

from app.schemas.settlement import (
    SettlementResponse,
    SettlementDetailsResponse
)
 
from app.repositories.settlement import (
    get_all_settlements
)
 

 
from app.models.tax_invoice import TaxInvoice
 
from app.schemas.tax_invoice import (
    TaxInvoiceListResponse,
    TaxInvoiceItem,
    TaxSummaryResponse
)
 
from sqlalchemy import select
from fastapi.responses import StreamingResponse

from sqlalchemy import select
from app.models.bank_transfer import BankTransfer
 
from app.schemas.bank_transfer import (
    BankTransferResponse,
    TransferItem,
    ReceivingAccount
)
 
from sqlalchemy import select
from fastapi.responses import StreamingResponse
 
from app.models.refund_deduction import RefundDeduction
 
from app.schemas.refund_deduction import (
    RefundDeductionResponse,
    RefundDeductionItem
)
 
from sqlalchemy import select
from sqlalchemy import or_
 
from fastapi import Query
from fastapi.responses import StreamingResponse
 

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


from sqlalchemy import select

@router.post("/bank-details")
async def save_bank_details(
    payload: RestaurantBankRequest,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Restaurant).where(Restaurant.id == payload.restaurant_id)
    )

    restaurant = result.scalar_one_or_none()

    if not restaurant:
        return {"error": "Restaurant not found"}

    restaurant.bank_account_holder = payload.bank_account_holder
    restaurant.bank_account_number = payload.bank_account_number
    restaurant.ifsc_code = payload.ifsc_code

    await db.commit()

    return {"message": "Bank details saved successfully"}
    
@router.post("/onboarding")
def restaurant_onboarding(

    restaurant_name: str = Form(...),

    cuisine_types: str = Form(...),

    opening_time: str = Form(...),
    closing_time: str = Form(...),

    address_line1: str = Form(...),

    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),

    latitude: float = Form(None),
    longitude: float = Form(None),

    is_draft: bool = Form(True),

    logo: UploadFile = File(None),

    db: AsyncSession = Depends(get_db)
):

    logo_filename = None

    if logo:
        logo_filename = logo.filename

    restaurant = Restaurant(

        restaurant_name=restaurant_name,

        cuisine_types=cuisine_types,

        opening_time=opening_time,
        closing_time=closing_time,

        address_line1=address_line1,

        city=city,
        state=state,
        pincode=pincode,

        latitude=latitude,
        longitude=longitude,

        logo_url=logo_filename,

        is_draft=is_draft
    )

    db.add(restaurant)

    db.commit()

    db.refresh(restaurant)

    return {
        "message": "Restaurant onboarding saved",
        "restaurant_id": str(restaurant.id),
        "logo": logo_filename
    }

    
@router.post("/documents")
async def upload_restaurant_documents(
    restaurant_id: str = Form(...),
    gst_certificate: UploadFile = File(None),
    fssai_license_file: UploadFile = File(None),
    cancelled_cheque: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):

    # Async query fix
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    restaurant = result.scalars().first()

    if not restaurant:
        return {"error": "Restaurant not found"}

    UPLOAD_DIR = "uploads/documents"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # GST FILE
    if gst_certificate:
        gst_path = f"{UPLOAD_DIR}/{gst_certificate.filename}"
        with open(gst_path, "wb") as buffer:
            shutil.copyfileobj(gst_certificate.file, buffer)

        restaurant.gst_certificate = gst_path

    # FSSAI FILE
    if fssai_license_file:
        fssai_path = f"{UPLOAD_DIR}/{fssai_license_file.filename}"
        with open(fssai_path, "wb") as buffer:
            shutil.copyfileobj(fssai_license_file.file, buffer)

        restaurant.fssai_license_file = fssai_path

    # CANCELLED CHEQUE
    if cancelled_cheque:
        cheque_path = f"{UPLOAD_DIR}/{cancelled_cheque.filename}"
        with open(cheque_path, "wb") as buffer:
            shutil.copyfileobj(cancelled_cheque.file, buffer)

        restaurant.cancelled_cheque = cheque_path

    # async commit
    await db.commit()

    return {
        "message": "Documents uploaded successfully"
    }
@router.post("/menu/add-item")
async def add_menu_item(

    restaurant_id: str = Form(...),
    item_name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    base_price: float = Form(...),
    tags: str = Form(None),
    tax_rate: str = Form(...),
    track_stock: bool = Form(True),
    combo_available: bool = Form(False),
    food_image: UploadFile = File(None),

    db: AsyncSession = Depends(get_db)
):

    UPLOAD_DIR = "uploads/menu"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    image_path = None

    if food_image:
        image_path = f"{UPLOAD_DIR}/{food_image.filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(food_image.file, buffer)

    item = MenuItem(
        restaurant_id=restaurant_id,
        item_name=item_name,
        description=description,
        category=category,
        base_price=base_price,
        tags=tags,
        tax_rate=tax_rate,
        track_stock=track_stock,
        combo_available=combo_available,
        image_url=image_path
    )

    db.add(item)

    await db.commit()
    await db.refresh(item)

    return {
        "message": "Menu item added successfully",
        "item_id": str(item.id)
    }

@router.post("/menu/bulk-upload")
async def bulk_upload_menu(
    restaurant_id: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    os.makedirs("uploads", exist_ok=True)

    temp_file = f"uploads/{file.filename}"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(temp_file)

    created_items = []

    for _, row in df.iterrows():

        try:
            item = MenuItem(
                restaurant_id=restaurant_id,
                item_name=str(row.get("item_name", "") or ""),
                description=str(row.get("description", "") or ""),
                category=str(row.get("category", "") or ""),
                base_price=float(row.get("base_price") or 0),
                tags=str(row.get("tags", "") or ""),
                tax_rate=str(row.get("tax_rate") or "0"),
                track_stock=str(row.get("track_stock", "false")).lower() == "true",
                combo_available=str(row.get("combo_available", "false")).lower() == "true"
            )

            db.add(item)
            await db.flush()   

            created_items.append({
                "id": str(item.id),
                "item_name": item.item_name
            })

        except Exception as e:
            created_items.append({
                "error": str(e),
                "row": str(row.to_dict())
            })

    await db.commit()

    return {
        "message": "Menu items uploaded successfully",
        "total_items": len(created_items),
        "items": created_items
    }
    
@router.get("/menu/{restaurant_id}", response_model=list[MenuItemOut])
async def get_menu(restaurant_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
    )

    return result.scalars().all()

@router.put("/menu/item/{item_id}/stock")
async def update_stock_status(
    item_id: str,
    is_available: bool,
    db: AsyncSession = Depends(get_db)
):

    item = await db.execute(select(MenuItem).filter(MenuItem.id == item_id))
    item = item.scalar_one_or_none()

    if not item:
        return {
            "error": "Menu item not found"
        }

    item.is_available = is_available

    await db.commit()

    return {
        "message": "Stock updated successfully"
    }
    
@router.put("/menu/item/{item_id}/stock")
async def update_stock_status(
    item_id: str,
    is_available: bool,
    db: AsyncSession = Depends(get_db)
):

    item = await db.execute(select(MenuItem).filter(MenuItem.id == item_id))
    item = item.scalar_one_or_none()

    if not item:
        return {
            "error": "Menu item not found"
        }

    item.is_available = is_available

    await db.commit()

    return {
        "message": "Stock updated successfully"
    }
    
@router.delete("/menu/item/{item_id}")
async def delete_menu_item(
    item_id: str,
    db: AsyncSession = Depends(get_db)
):

    item = await db.execute(select(MenuItem).filter(MenuItem.id == item_id))
    item = item.scalar_one_or_none()

    if not item:
        return {
            "error": "Menu item not found"
        }

    db.delete(item)

    await db.commit()

    return {
        "message": "Menu item deleted successfully"
    }
    
@router.post("/combos")
async def create_meal_combo(
    restaurant_id: str = Form(...),
    combo_name: str = Form(...),
    description: str = Form(...),
    combo_price: float = Form(...),
    tags: str = Form(None),
    combo_image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):

    import os, shutil

    UPLOAD_DIR = "uploads/combos"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    image_path = None

    if combo_image:
        image_path = f"{UPLOAD_DIR}/{combo_image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(combo_image.file, buffer)

    combo = MealCombo(
        restaurant_id=restaurant_id,
        combo_name=combo_name,
        description=description,
        combo_price=combo_price,
        tags=tags,
        image_url=image_path
    )

    db.add(combo)

    await db.commit()
    await db.refresh(combo)

    return {
        "message": "Meal combo created successfully",
        "combo_id": combo.id
    }
    
@router.get("/combos/{restaurant_id}")
async def get_combos(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MealCombo).where(MealCombo.restaurant_id == restaurant_id)
    )

    combos = result.scalars().all()

    return combos

@router.delete("/combos/{combo_id}")
async def delete_combo(
    combo_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MealCombo).where(MealCombo.id == combo_id)
    )

    combo = result.scalars().first()

    if not combo:
        return {"error": "Combo not found"}

    await db.delete(combo)
    await db.commit()

    return {"message": "Combo deleted successfully"}

@router.post("/customization-groups")
async def create_customization_group(
    restaurant_id: str,
    group_name: str,
    db: AsyncSession = Depends(get_db)
):

    group = CustomizationGroup(
        restaurant_id=restaurant_id,
        group_name=group_name
    )

    db.add(group)

    await db.commit()
    await db.refresh(group)

    return {
        "message": "Customization group created",
        "group_id": group.id
    }
    
@router.post("/customization-options")
async def create_customization_option(
    group_id: str,
    option_name: str,
    extra_price: float,
    db: AsyncSession = Depends(get_db)
):

    option = CustomizationOption(
        group_id=group_id,
        option_name=option_name,
        extra_price=extra_price
    )

    db.add(option)

    await db.commit()
    await db.refresh(option)

    return {
        "message": "Option added successfully",
        "option_id": option.id
    }
    
@router.get("/customization-groups/{restaurant_id}")
async def get_customization_groups(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    # Get all groups
    result = await db.execute(
        select(CustomizationGroup).where(
            CustomizationGroup.restaurant_id == restaurant_id
        )
    )

    groups = result.scalars().all()

    response = []

    for group in groups:

        # Get options for each group
        option_result = await db.execute(
            select(CustomizationOption).where(
                CustomizationOption.group_id == group.id
            )
        )

        options = option_result.scalars().all()

        response.append({
            "group_id": group.id,
            "group_name": group.group_name,
            "options": options
        })

    return response

@router.post("/pricing-analytics")
async def create_pricing_analytics(
    restaurant_id: str,
    increase_percentage: float,
    message: str,
    db: AsyncSession = Depends(get_db)
):

    analytics = PricingAnalytics(
        restaurant_id=restaurant_id,
        increase_percentage=increase_percentage,
        message=message
    )

    db.add(analytics)

    await db.commit()
    await db.refresh(analytics)

    return {
        "message": "Pricing analytics created successfully",
        "analytics_id": analytics.id,
        "increase_percentage": increase_percentage
    }

@router.put("/menu/item/{item_id}/pricing")
async def update_menu_pricing(

    item_id: str,
    base_price: float,
    tax_category: str,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MenuItem).where(MenuItem.id == item_id)
    )

    item = result.scalars().first()

    if not item:
        return {
            "error": "Menu item not found"
        }

    item.base_price = base_price
    item.tax_category = tax_category

    await db.commit()
    await db.refresh(item)

    return {
        "message": "Pricing updated successfully",
        "item_id": item.id,
        "base_price": item.base_price,
        "tax_category": item.tax_category
    }
    
@router.post("/pricing-rules")
async def create_pricing_rule(

    menu_item_id: str,
    rule_name: str,
    adjustment_type: str,
    adjustment_value: float,
    start_date: str,
    end_date: str,
    active_days: str = None,

    db: AsyncSession = Depends(get_db)
):

    rule = PricingRule(
        menu_item_id=menu_item_id,
        rule_name=rule_name,
        adjustment_type=adjustment_type,
        adjustment_value=adjustment_value,
        start_date=start_date,
        end_date=end_date,
        active_days=active_days
    )

    db.add(rule)

    await db.commit()
    await db.refresh(rule)

    return {
        "message": "Pricing rule created",
        "rule_id": rule.id
    }
    
@router.get("/pricing-rules/{menu_item_id}")
async def get_pricing_rules(
    menu_item_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(PricingRule).where(
            PricingRule.menu_item_id == menu_item_id
        )
    )

    rules = result.scalars().all()

    return rules

@router.delete("/pricing-rules/{rule_id}")
async def delete_pricing_rule(
    rule_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(PricingRule).where(
            PricingRule.id == rule_id
        )
    )

    rule = result.scalars().first()

    if not rule:
        return {"error": "Pricing rule not found"}

    await db.delete(rule)
    await db.commit()

    return {"message": "Pricing rule deleted"}

@router.post("/menu-schedule")
async def create_menu_schedule(
    menu_item_id: str,
    day_of_week: str,
    start_time: str,
    end_time: str,
    service_name: str,
    db: AsyncSession = Depends(get_db)
):

    schedule = MenuSchedule(
        menu_item_id=menu_item_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        service_name=service_name
    )

    db.add(schedule)

    await db.commit()
    await db.refresh(schedule)

    return {
        "message": "Schedule created",
        "schedule_id": schedule.id
    }
    
@router.get("/menu-schedule/{menu_item_id}")
async def get_menu_schedule(
    menu_item_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MenuSchedule).where(
            MenuSchedule.menu_item_id == menu_item_id
        )
    )

    schedules = result.scalars().all()

    return schedules


@router.post("/gallery/upload")
async def upload_images(
    restaurant_id: str = Form(...),
    files: Optional[List[UploadFile]] = File(None)
):
    UPLOAD_DIR = "uploads/gallery"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    saved_files = []

    if files:
        for file in files:
            if not file.filename:
                continue

            file_path = os.path.join(UPLOAD_DIR, file.filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            saved_files.append(file.filename)

    return {
        "restaurant_id": restaurant_id,
        "uploaded_files": saved_files
    }
    
@router.get("/gallery/{restaurant_id}")
async def get_gallery(
    restaurant_id: str,
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * limit

    result = await db.execute(
        select(Gallery)
        .where(Gallery.restaurant_id == restaurant_id)
        .offset(offset)
        .limit(limit)
    )

    images = result.scalars().all()

    return images

@router.put("/gallery/assign")
async def assign_image(
    image_id: str,
    menu_item_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Gallery).where(Gallery.id == image_id)
    )

    image = result.scalars().first()

    if not image:
        return {"error": "Image not found"}

    image.menu_item_id = menu_item_id
    image.is_assigned = True

    await db.commit()

    return {"message": "Assigned successfully"}
    
@router.put("/gallery/unassign/{image_id}")
async def unassign_image(
    image_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Gallery).where(Gallery.id == image_id)
    )

    image = result.scalars().first()

    if not image:
        return {"error": "Image not found"}

    image.menu_item_id = None
    image.is_assigned = False

    await db.commit()

    return {"message": "Unassigned"}
    
@router.delete("/gallery/{image_id}")
async def delete_image(
    image_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Gallery).where(Gallery.id == image_id)
    )

    image = result.scalars().first()

    if not image:
        return {"error": "Image not found"}

    await db.delete(image)
    await db.commit()

    return {"message": "Deleted successfully"}

@router.get("/orders/{restaurant_id}")
async def get_incoming_orders(
    restaurant_id: UUID,   
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order).where(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.pending
        )
    )

    orders = result.scalars().all()   

    return orders

@router.post("/orders/{order_id}/accept")
async def accept_order(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.status = "accepted"

    await db.commit()

    return {"message": "Order accepted"}


@router.post("/orders/{order_id}/reject")
async def reject_order(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.status = "rejected"

    await db.commit()

    return {"message": "Order rejected"}


@router.put("/orders/{order_id}/status")
async def update_status(order_id: int, status: str, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.status = status

    await db.commit()

    return {"message": "Status updated"}

@router.get("/orders/{restaurant_id}/stats")
async def get_order_stats(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    
    total_result = await db.execute(
        select(func.count()).where(
            Order.restaurant_id == restaurant_id
        )
    )

    total_orders = total_result.scalar() or 0

    
    completed_result = await db.execute(
        select(func.count()).where(
            Order.restaurant_id == restaurant_id,
            Order.status == OrderStatus.completed
        )
    )

    completed_orders = completed_result.scalar() or 0

    avg_prep_time = 12.4

    efficiency = (
        round((completed_orders / total_orders) * 100, 2)
        if total_orders else 0
    )

    return {
        "avg_prep_time": avg_prep_time,
        "orders_fulfilled": completed_orders,
        "efficiency_score": efficiency
    }


@router.get("/orders/history/{restaurant_id}")
async def order_history(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.restaurant_id == restaurant_id)
        .order_by(Order.created_at.desc())
    )

    orders = result.scalars().all()

    return [
        {
            "id": o.id,
            "items": [
                {
                    "name": item.name,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in o.items
            ],
            "subtotal": o.subtotal,
            "tax_percent": o.tax_percent,
            "total": o.total,
            "status": o.status,
            "order_time": o.order_time,
            "created_at": o.created_at,
            "prep_time": o.prep_time,
            "is_urgent": o.is_urgent,
            "delivery_address": o.delivery_address,
            "courier_name": o.courier_name,
            "courier_rating": o.courier_rating,
            "completed_at": o.completed_at
        }
        for o in orders
    ]
@router.get("/orders/{order_id}/receipt")
async def get_receipt(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Items
    items = [
        {
            "menu_item_id": item.menu_item_id,
            "quantity": item.quantity,
            "price": item.price
        }
        for item in (order.items or [])
    ]

    # Safe numeric values
    subtotal = sum(i["price"] * i["quantity"] for i in items)
    delivery_fee = float(order.delivery_fee or 0)
    tax_percent = float(order.tax_percent or 0)

    tax = subtotal * (tax_percent / 100)
    total = subtotal + delivery_fee + tax

    return {
        "receipt_id": f"REC-{order.id}",
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "tax": tax,
        "total": total,
        "status": order.status
    }
    
@router.get("/orders/{order_id}/timeline")
async def order_timeline(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    return [
        {"stage": "Order Placed", "status": "done"},
        {"stage": "Accepted by Kitchen", "status": "done"},
        {"stage": "Preparing", "status": "done"},
        {"stage": "Out for Delivery", "status": "done"},
        {"stage": "Delivered", "status": "done"}
    ]

@router.get("/orders/search/{restaurant_id}")
async def search_orders(
    restaurant_id: str,
    query: str = Query(...),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order)
        .join(Order.items)
        .options(selectinload(Order.items))
        .where(
            Order.restaurant_id == restaurant_id,
            OrderItem.name.ilike(f"%{query}%")
        )
        .distinct()
    )

    orders = result.scalars().all()

    return orders

@router.get("/kitchen/active/{restaurant_id}")
async def active_kitchen_orders(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(
            Order.restaurant_id == restaurant_id,
            Order.status.in_(["accepted", "preparing"])  # use enum if defined
        )
        .order_by(Order.created_at.asc())  # oldest first (kitchen priority)
    )

    orders = result.scalars().all()

    result_list = []

    now = datetime.now(timezone.utc)  

    for o in orders:

        remaining = None

        
        if o.start_time and o.prep_time:
            elapsed = (now - o.start_time).total_seconds() / 60
            remaining = max(o.prep_time - int(elapsed), 0)

        
        items = [
            {
                "name": item.name,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in o.items
        ] if o.items else []

        
        if remaining is None:
            urgency = "normal"
        elif remaining <= 5:
            urgency = "high"
        elif remaining <= 10:
            urgency = "medium"
        else:
            urgency = "normal"

        result_list.append({
            "order_id": o.id,
            "items": items,
            "prep_time_total": o.prep_time,
            "remaining_minutes": remaining,
            "urgency": urgency,
            "status": o.status,
            "start_time": o.start_time   
        })

    return result_list

@router.post("/kitchen/start/{order_id}")
async def start_cooking(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.status = OrderStatus.preparing   
    order.start_time = datetime.utcnow()

    await db.commit()

    return {"message": "Cooking started"}

@router.put("/kitchen/urgency/{order_id}")
async def set_urgency(order_id: int, level: str, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.is_urgent = level  # normal / urgent / extreme

    await db.commit()

    return {"message": "Urgency updated"}

@router.put("/kitchen/prep-time/{order_id}")
async def set_prep_time(order_id: int, minutes: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.prep_time = minutes

    await db.commit()

    return {"message": "Prep time set"}

@router.post("/kitchen/pack/{order_id}")
async def mark_as_packed(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.status = OrderStatus.packed

    await db.commit()

    return {"message": "Order marked packed"}

@router.get("/kitchen/qc/{order_id}")
async def quality_check(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    tax = (order.subtotal * order.tax_percent) / 100

    return {
        "order_id": order.id,
        "items": order.items,
        "special_instructions": order.special_instructions,
        "extras": order.extras,
        "cutlery_required": order.cutlery_required,
        "packaging_notes": order.packaging_notes,
        "subtotal": order.subtotal,
        "tax": round(tax, 2),
        "delivery_fee": order.delivery_fee,
        "total": round(order.subtotal + tax + order.delivery_fee, 2)
    }

@router.post("/kitchen/pack/{order_id}")
async def mark_as_packed(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.status = OrderStatus.packed

    await db.commit()

    return {
        "message": "Order marked as packed"
    }

@router.put("/kitchen/notes/{order_id}") 
async def update_notes(order_id: int, note: str, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.special_instructions = note

    await db.commit()

    return {"message": "Notes updated"}


@router.put("/kitchen/extras/{order_id}")
async def update_extras(
    order_id: int,
    extras: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    order.extras = extras

    await db.commit()

    return {"message": "Extras updated"}

@router.get("/kitchen/receipt/{order_id}")
async def print_receipt(order_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        return {"error": "Order not found"}

    tax = (order.subtotal * order.tax_percent) / 100
    total = order.subtotal + tax + order.delivery_fee

    return {
        "receipt": {
            "order_id": order.id,
            "subtotal": order.subtotal,
            "tax": round(tax, 2),
            "delivery": order.delivery_fee,
            "total": round(total, 2),
            "status": order.status
        }
    }
    
    
    
 
from app.schemas.restaurant import (
    IngredientCreate,
    IngredientOut,
    IngredientPriceUpdate,
    WasteCreate,
)
from app.models.restaurant import (
    Ingredient,
    IngredientWaste,
    MenuIngredient,
    InventoryAdjustment
)


import traceback
 
@router.post("/ingredients", response_model=IngredientOut)
async def create_ingredient(data: IngredientCreate, db: AsyncSession = Depends(get_db)):
 
    try:
        ingredient = Ingredient(**data.dict())
 
        db.add(ingredient)
        await db.flush()
        await db.commit()
        await db.refresh(ingredient)
 
        return ingredient
 
    except Exception as e:
        print("CREATE INGREDIENT ERROR:")
        print(traceback.format_exc())
        raise HTTPException(
        status_code=500,
        detail="Internal server error while creating ingredient"
    )
   
@router.get(
    "/ingredients/{ingredient_id}",
    response_model=IngredientOut
)
async def ingredient_details(
    ingredient_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Ingredient).where(
            Ingredient.id == ingredient_id
        )
    )
 
    ingredient = result.scalar_one_or_none()
 
    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )
 
    return ingredient
 
 
@router.put("/ingredients/{ingredient_id}/price")
async def update_price(
    ingredient_id: UUID,
    data: IngredientPriceUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Ingredient).where(
            Ingredient.id == ingredient_id
        )
    )
 
    ingredient = result.scalar_one_or_none()
 
    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )
 
    ingredient.last_price = ingredient.current_price
 
    ingredient.price_change = round(
        data.current_price - ingredient.current_price,
    )
 
    ingredient.current_price = data.current_price
 
    await db.commit()
 
    return {
        "message": "Price updated"
    }
 
@router.post("/ingredients/{ingredient_id}/waste")
async def add_waste(
    ingredient_id: UUID,
    data: WasteCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Ingredient).where(
            Ingredient.id == ingredient_id
        )
    )
 
    ingredient = result.scalar_one_or_none()
 
    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )
 
    waste = IngredientWaste(
        ingredient_id=ingredient_id,
        units_spoiled=data.units_spoiled,
        reason=data.reason,
        loss_amount=data.loss_amount
    )
 
    ingredient.stock_units -= data.units_spoiled
    db.add(waste)
    await db.commit()
 
    return {
        "message": "Waste log added"
    }
 
 
@router.post("/ingredients/{ingredient_id}/sync-menu")
async def sync_menu_availability(
    ingredient_id: UUID ,
    db: AsyncSession = Depends(get_db)
):
   
    ingredient_result = await db.execute(
        select(Ingredient).where(
            Ingredient.id == ingredient_id
        )
    )
 
    ingredient = ingredient_result.scalar_one_or_none()
 
    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingredient not found"
        )
 
    menu_links_result = await db.execute(
        select(MenuIngredient).where(
            MenuIngredient.ingredient_id == ingredient_id
        )
    )
 
    links = menu_links_result.scalars().all()
 
    for link in links:
 
        menu_result = await db.execute(
            select(MenuItem).where(
                MenuItem.id == link.menu_item_id
            )
        )
 
        menu_item = menu_result.scalar_one_or_none()
 
        if menu_item:
 
            if ingredient.stock_units <= 0:
                menu_item.is_available = False
 
            else:
                menu_item.is_available = True
 
    await db.commit()
 
    return {
        "message": "Menu availability synced"
    }
 
@router.get("/inventory/alerts/{restaurant_id}")
async def inventory_alerts(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Ingredient).where(
            Ingredient.restaurant_id == restaurant_id
        )
    )
 
    ingredients = result.scalars().all()
 
    alerts = []
 
    for item in ingredients:
 
        # OUT OF STOCK
        if item.stock_units <= 0:
 
            item.is_out_of_stock = True
            item.is_low_stock = False
 
            alerts.append({
                "ingredient": item.ingredient_name,
                "status": "OUT OF STOCK",
                "message": f"{item.ingredient_name} is finished"
            })
 
        # LOW STOCK
        elif item.stock_units <= item.min_threshold:
 
            item.is_low_stock = True
            item.is_out_of_stock = False
 
            alerts.append({
                "ingredient": item.ingredient_name,
                "status": "LOW STOCK",
                "current_stock": item.stock_units,
                "threshold": item.min_threshold,
                "message": f"Only {item.stock_units} left"
            })
 
        else:
 
            item.is_low_stock = False
            item.is_out_of_stock = False
 
    await db.commit()
 
    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }
@router.get("/inventory/status/{restaurant_id}")
async def stock_status(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Ingredient).where(
            Ingredient.restaurant_id == restaurant_id
        )
    )
 
    ingredients = result.scalars().all()
 
    total_items = len(ingredients)
 
    safe_items = 0
 
    for item in ingredients:
 
        if item.stock_units > item.min_threshold:
            safe_items += 1
 
    percentage = 0
 
    if total_items > 0:
        percentage = round(
            (safe_items / total_items) * 100,
            2
        )
 
    return {
        "safe_inventory_percentage": percentage,
        "total_items": total_items,
        "safe_items": safe_items
    }
@router.put("/inventory/update-stock")
async def update_inventory_stock(
 
    ingredient_id: UUID,
 
    new_quantity: float,
 
    reason: str,
 
    updated_by: str,
 
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Ingredient).where(
            Ingredient.id == ingredient_id
        )
    )
 
    ingredient = result.scalar_one_or_none()
 
    if not ingredient:
        return {
            "error": "Ingredient not found"
        }
 
    adjustment = InventoryAdjustment(
        ingredient_id=ingredient.id,
        ingredient_name=ingredient.ingredient_name,
        previous_quantity=ingredient.stock_units,
        new_quantity=new_quantity,
        reason=reason,
        updated_by=updated_by
    )
    ingredient.stock_units = new_quantity
    db.add(adjustment)
 
    await db.commit()
 
    return {
        "message": "Inventory updated"
    }
@router.get("/inventory/adjustments")
async def inventory_adjustments(
    db: AsyncSession = Depends(get_db)
):
 
    result_db = await db.execute(
        select(InventoryAdjustment)
    )
 
    data = result_db.scalars().all()
 
    result = []
 
    for item in data:
 
        result.append({
            "ingredient": item.ingredient_name,
            "old_quantity": item.previous_quantity,
            "new_quantity": item.new_quantity,
            "reason": item.reason,
            "updated_by": item.updated_by,
            "time": item.created_at
        })
 
    return result
 
from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.schemas.coupon import (
    CouponCreate,
    CouponOut,
)
from app.services.coupon_service import CouponService
from app.repositories.coupon_repository import CouponRepository
 
from fastapi import Header, HTTPException
 
async def get_current_restaurant(restaurant_id: str = Header(None)):
    if not restaurant_id:
        raise HTTPException(status_code=401, detail="restaurant_id missing")
    try:
        return {"restaurant_id": UUID(restaurant_id)}
    except:
        raise HTTPException(status_code=400, detail="Invalid restaurant_id")
   
 
@router.post("/coupons/create",response_model=CouponOut)
async def create_coupon(
    coupon_data: CouponCreate,
    db: AsyncSession = Depends(get_db),
    current_restaurant = Depends(get_current_restaurant),
):
 
    return await CouponService.create_coupon(
        db=db,
        restaurant_id=current_restaurant["restaurant_id"],
        coupon_data=coupon_data,
    )
 
 
 
@router.get(
    "/coupons/restaurant/{restaurant_id}",
    response_model=list[CouponOut]
)
async def get_restaurant_coupons(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db),
):
 
    return await CouponRepository.get_restaurant_coupons(
        db,
        restaurant_id,
    )
 
 
@router.post("/coupons/validate")
async def validate_coupon(
    coupon_code: str,
    order_amount: float,
    db: AsyncSession = Depends(get_db),
):
 
    return await CouponService.validate_coupon(
        db,
        coupon_code,
        order_amount,
    )
 
from app.services.campaign_service import CampaignService
from app.utils.enums import CampaignStatus
 
from app.schemas.campaign_schema import CampaignUpdate
from app.models.restaurant import Restaurant
from app.schemas.campaign_schema import (
    CampaignCreate,
    CampaignOut
)
@router.post("/", response_model=CampaignOut)
async def create_campaign(
    payload: CampaignCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
 
        result = await db.execute(
            select(Restaurant)
        )
 
        restaurant = result.scalars().first()
 
        print("Restaurant:", restaurant)
 
        if not restaurant:
            raise HTTPException(
                status_code=404,
                detail="No restaurant found in database"
            )
 
        campaign = await CampaignService.create_campaign(
            db=db,
            payload=payload,
            restaurant_id=restaurant.id
        )
 
        print("Campaign:", campaign)
 
        return campaign
 
    except Exception as e:
        print("FULL ERROR:", repr(e))
        raise e
 
@router.get("/", response_model=list[CampaignOut])
async def get_campaigns(
    db: AsyncSession = Depends(get_db)
):
 
    campaigns = await CampaignService.get_all_campaigns(db)
 
    return campaigns
 
 
from app.services.campaign_service import DashboardService as CampaignDashboardService 
@router.get("/summary")
async def dashboard_summary(
    db: AsyncSession = Depends(get_db)
):
 
    summary = await DashboardService.get_summary(db)
 
    return summary
 
@router.get("/scheduled-campaigns")
async def scheduled_campaigns(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Campaign)
        .where(Campaign.status == CampaignStatus.SCHEDULED)
        .order_by(Campaign.start_date.asc())
    )
    return result.scalars().all()
 
 
@router.get("/analytics")
async def analytics_dashboard(
    db: AsyncSession = Depends(get_db)
):
 
    analytics = await DashboardService.get_analytics(db)
 
    return analytics
 
@router.get("/campaign/{campaign_id}", response_model=CampaignOut)
async def get_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    campaign = await CampaignService.get_campaign_by_id(db, campaign_id)

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return campaign
 
@router.patch("/campaign/{campaign_id}")
async def update_campaign(
    campaign_id: UUID,
    payload: CampaignUpdate,
    db: AsyncSession = Depends(get_db)
):
 
    campaign = await CampaignService.get_campaign_by_id(
        db,
        campaign_id
    )
 
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )
 
    updated_campaign = await CampaignService.update_campaign(
        db,
        campaign,
        payload
    )
 
    return updated_campaign
 
@router.patch("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    campaign = await CampaignService.get_campaign_by_id(
        db,
        campaign_id
    )
 
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )
 
    campaign.status = CampaignStatus.PAUSED
 
    await db.commit()
 
    return {
        "message": "Campaign paused successfully"
    }
 
@router.patch("/{campaign_id}/activate")
async def activate_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    campaign = await CampaignService.get_campaign_by_id(
        db,
        campaign_id
    )
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )
 
    campaign.status = CampaignStatus.ACTIVE
 
    await db.commit()
 
    return {
        "message": "Campaign activated successfully"
    }
 
@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    campaign = await CampaignService.get_campaign_by_id(
        db,
        campaign_id
    )
 
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )
 
    await CampaignService.delete_campaign(
        db,
        campaign
    )
 
    return {
        "message": "Campaign deleted successfully"
    }
 

from sqlalchemy import text
from app.models.campaign import Campaign
@router.put("/campaign/{campaign_id}/smart-bidding")
async def toggle_smart_bidding(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id)
    )
 
    campaign = result.scalar_one_or_none()
 
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )
 
    campaign.smart_bidding = not campaign.smart_bidding
 
    await db.commit()
    await db.refresh(campaign)
 
    return {
        "message": "Smart bidding updated",
        "smart_bidding": campaign.smart_bidding
    }
 
 
 
@router.put("/campaign/{campaign_id}/budget")
async def update_budget(
    campaign_id: UUID,
    daily: float,
    total: float,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id)
    )
 
    campaign = result.scalar_one_or_none()
 
    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )
 
    campaign.daily_budget = daily
    campaign.total_budget = total
 
    await db.commit()
    await db.refresh(campaign)
 
    return {
        "message": "Budget updated",
        "daily_budget": campaign.daily_budget,
        "total_budget": campaign.total_budget
    }
 
 
@router.get("/customer-analytics/retention/{restaurant_id}")
async def retention_mix(
    restaurant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
 
    total_result = await db.execute(
        select(func.count(func.distinct(Order.user_id)))
        .where(Order.restaurant_id == restaurant_id)
    )
 
    total_customers = total_result.scalar() or 0
 
    returning_result = await db.execute(
        select(func.count(func.distinct(Order.user_id)))
        .where(
            Order.restaurant_id == restaurant_id,
            Order.visit_count > 1
        )
    )
 
    returning_customers = returning_result.scalar() or 0
 
    new_customers = total_customers - returning_customers
 
    retention_percentage = 0
 
    if total_customers > 0:
        retention_percentage = round(
            (returning_customers / total_customers) * 100,
            2
        )
 
    return {
 
        "returning_customers": returning_customers,
 
        "new_customers": new_customers,
 
        "retention_percentage": retention_percentage
    }
 
# AVERAGE RATING
 
@router.get("/customer-analytics/rating/{restaurant_id}")
async def average_rating(
    restaurant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(func.avg(Order.rating))
        .where(Order.restaurant_id == restaurant_id)
    )
 
    avg_rating = result.scalar() or 0
 
    return {
        "average_rating": round(avg_rating, 1)
    }
 
# VISIT FREQUENCY
 
@router.get("/customer-analytics/visit-frequency/{restaurant_id}")
async def visit_frequency(
    restaurant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(func.avg(Order.visit_count))
        .where(Order.restaurant_id == restaurant_id)
    )
 
    frequency = result.scalar() or 0
 
    return {
        "visit_frequency": round(frequency, 1)
    }
 
# VIP CUSTOMERS

@router.get("/customer-analytics/vip-customers/{restaurant_id}")
async def vip_customers(
    restaurant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(
            User.full_name.label("customer_name"),
            func.sum(Order.total).label("total_spend"),
            func.count(Order.id).label("visits")
        )
        .join(Order, Order.user_id == User.id)
        .where(Order.restaurant_id == restaurant_id)
        .group_by(User.id, User.full_name)
        .order_by(func.sum(Order.total).desc())
        .limit(5)
    )

    return [
        {
            "customer_name": row.customer_name,
            "total_spend": float(row.total_spend or 0),
            "visits": row.visits
        }
        for row in result.all()
    ]
# FEEDBACK HIGHLIGHTS
 
@router.get("/customer-analytics/feedbacks/{restaurant_id}")
async def feedbacks(
    restaurant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
 
        select(
            Order.review,
            Order.rating
        )
 
        .where(
            Order.restaurant_id == restaurant_id,
            Order.review.isnot(None)
        )
 
        .limit(10)
    )
 
    feedback_list = []
 
    for row in result.all():
 
        feedback_list.append({
 
            "review": row.review,
 
            "rating": row.rating
        })
 
    return feedback_list
 
 # COMPLETE DASHBOARD
 
@router.get("/dashboard/{restaurant_id}")
async def dashboard(
 
    restaurant_id: str,
 
    db: AsyncSession = Depends(get_db)
):
 
    data = await get_dashboard_data(
        db,
        restaurant_id
    )
 
    return data
 
# TOP SELLING ITEMS
 
@router.get("/top-selling/{restaurant_id}")
async def top_selling(
 
    restaurant_id: str,
 
    db: AsyncSession = Depends(get_db)
):
 
    data = await get_top_selling_by_quantity(
        db,
        restaurant_id
    )
 
    return data
 
# TOP REVENUE ITEMS
 
@router.get("/top-revenue/{restaurant_id}")
async def top_revenue(
 
    restaurant_id: str,
 
    db: AsyncSession = Depends(get_db)
):
 
    data = await get_top_selling_by_revenue(
        db,
        restaurant_id
    )
 
    return data
 
# CATEGORY INSIGHTS
 
@router.get("/category-insights/{restaurant_id}")
async def category_insights(
 
    restaurant_id: str,
 
    db: AsyncSession = Depends(get_db)
):
 
    data = await get_category_insights(
        db,
        restaurant_id
    )
 
    return data
 
# MENU RANKINGS
 
@router.get("/menu-rankings/{restaurant_id}")
async def menu_rankings(
 
    restaurant_id: str,
 
    db: AsyncSession = Depends(get_db)
):
 
    data = await get_menu_rankings(
        db,
        restaurant_id
    )
 
    return data

# ALWAYS put fixed routes FIRST
@router.get("/metrics")
async def get_metrics(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    print("DashboardService =", DashboardService)
    print("Module =", DashboardService.__module__)
    print("Methods =", dir(DashboardService))

    return await DashboardService.get_metrics(
        session,
        restaurant_id
    )

@router.get("/repeat-orders")
async def repeat_orders(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.repeat_orders(session, restaurant_id)


@router.get("/market-reach")
async def market_reach(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.market_reach(session, restaurant_id)


@router.get("/rating-trend")
async def rating_trend(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.rating_trend(session, restaurant_id)



@router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await CampaignService.get_campaign_by_id(db, campaign_id)
 
@router.get("/growth-tips/{restaurant_id}")
async def growth_tips(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.growth_tips(session, restaurant_id)
 
 
@router.get("/competitor-benchmark/{restaurant_id}")
async def competitor_benchmark(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.competitor_benchmark(session, restaurant_id)
 
 
@router.get("/marketing-impact/{restaurant_id}")
async def marketing_impact(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.marketing_impact(session, restaurant_id)
 
 
@router.get("/stock-efficiency/{restaurant_id}")
async def stock_efficiency(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.stock_efficiency(session, restaurant_id)
 
 
@router.get("/staff-performance/{restaurant_id}")
async def staff_performance(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DashboardService.staff_performance(session, restaurant_id)
 
 
 
 
 
@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
async def dashboard_summary(
    restaurant_id: UUID,
    session: AsyncSession = Depends(get_db)
):
 
    return await DashboardService.dashboard_summary(
        session,
        restaurant_id
    )
    
# CREATE REVENUE REPORT
 
@router.post("/create")
async def create_revenue_report(
 
    restaurant_id: UUID,
 
    total_revenue: float,
 
    total_orders: int,
 
    avg_order_value: float,
 
    gst_amount: float,
 
    platform_commission: float,
 
    delivery_fee: float,
 
    net_earnings: float,
 
    digital_payments: float,
 
    card_payments: float,
 
    cash_on_delivery: float,
 
    db: AsyncSession = Depends(get_db)
):
 
    report = RevenueReport(
 
        restaurant_id=restaurant_id,
 
        total_revenue=total_revenue,
 
        total_orders=total_orders,
 
        avg_order_value=avg_order_value,
 
        gst_amount=gst_amount,
 
        platform_commission=platform_commission,
 
        delivery_fee=delivery_fee,
 
        net_earnings=net_earnings,
 
        digital_payments=digital_payments,
 
        card_payments=card_payments,
 
        cash_on_delivery=cash_on_delivery
    )
 
    db.add(report)
 
    await db.commit()
 
    await db.refresh(report)
 
    return {
        "message": "Revenue report created",
        "report_id": str(report.id)
    }
 
@router.get("/revenue/{restaurant_id}")
async def get_revenue_report(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    print("=== HIT ENDPOINT ===")
    print("restaurant_id:", restaurant_id)

    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.restaurant_id == restaurant_id
        )
    )

    report = result.scalars().first()

    print("REPORT:", report)

    return report

# UPDATE REPORT
 
@router.put("/{report_id}")
async def update_revenue_report(
 
    report_id: UUID,
 
    total_revenue: float,
 
    net_earnings: float,
 
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.id == report_id
        )
    )
 
    report = result.scalar_one_or_none()
 
    if not report:
        return {
            "message": "Report not found"
        }
 
    report.total_revenue = total_revenue
    report.net_earnings = net_earnings
 
    await db.commit()
 
    return {
        "message": "Revenue report updated"
    }
 
# DELETE REPORT
 
@router.delete("/{report_id}")
async def delete_revenue_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.id == report_id
        )
    )
 
    report = result.scalar_one_or_none()
 
    if not report:
        return {
            "message": "Report not found"
        }
 
    await db.delete(report)
 
    await db.commit()
 
    return {
        "message": "Revenue report deleted"
    }
 
# REVENUE HISTORY
 
@router.get("/history/{restaurant_id}")
async def revenue_history(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.restaurant_id == restaurant_id
        )
    )
 
    reports = result.scalars().all()
 
    return reports
 
# PAYMENT METHODS
 
@router.get("/payment-methods/{restaurant_id}")
async def payment_methods(
    restaurant_id: UUID,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RevenueReport).where(
            RevenueReport.restaurant_id == restaurant_id
        )
    )
 
    report = result.scalar_one_or_none()
 
    if not report:
        return {
            "message": "No data found"
        }
 
    return {
 
        "digital_payments": report.digital_payments,
 
        "card_payments": report.card_payments,
 
        "cash_on_delivery": report.cash_on_delivery
    }  
    
async def get_settlements(
    search: str = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
 
    settlements = await get_all_settlements(
        db=db,
        search=search
    )
 
    return {
        "current_period_amount": 14582.40,
        "next_payout_amount": 2410.15,
        "processing_percentage": 65,
        "estimated_date": "Nov 5",
        "settlements": settlements
    }
 
 
# @router.get("/export/csv")
# async def export_csv(
#     db: AsyncSession = Depends(get_db)
# ):
 
#     settlements = await get_all_settlements(db)
 
#     file_path = "settlements.csv"
 
#     with open(
#         file_path,
#         mode="w",
#         newline="",
#         encoding="utf-8"
#     ) as csv_file:
 
#         writer = csv.writer(csv_file)
 
#         writer.writerow([
#             "Settlement ID",
#             "Cycle",
#             "Gross Sales",
#             "Deductions",
#             "Net Payout",
#             "Status"
#         ])
 
#         for settlement in settlements:
 
#             writer.writerow([
#                 settlement.settlement_id,
#                 settlement.cycle,
#                 settlement.gross_sales,
#                 settlement.deductions,
#                 settlement.net_payout,
#                 settlement.status
#             ])
 
#     return FileResponse(
#         path=file_path,
#         filename="settlements.csv",
#         media_type="text/csv"
#     )
 
 
 
@router.get(
    "/settlements",
    response_model=SettlementResponse
)
async def get_settlements(
    search: str = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
 
    query = select(Settlement)
 
    # SEARCH
    if search:
        query = query.where(
            Settlement.settlement_id.ilike(f"%{search}%")
        )
 
    result = await db.execute(query)
 
    settlements = result.scalars().all()
 
    return {
        "current_period_amount": 14582.40,
        "next_payout_amount": 2410.15,
        "processing_percentage": 65,
        "estimated_date": "Nov 5",
        "settlements": settlements
    }
@router.get(
    "/settlements/export/csv"
)
async def export_settlement_csv(
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Settlement)
    )
 
    settlements = result.scalars().all()
 
    output = StringIO()
 
    writer = csv.writer(output)
 
    writer.writerow([
        "Settlement ID",
        "Cycle",
        "Gross Sales",
        "Deductions",
        "Net Payout",
        "Status"
    ])
 
    for settlement in settlements:
 
        writer.writerow([
            settlement.settlement_id,
            settlement.cycle,
            settlement.gross_sales,
            settlement.deductions,
            settlement.net_payout,
            settlement.status
        ])
 
    output.seek(0)
 
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=settlements.csv"
        }
    )
@router.get(
    "/settlements/{settlement_id}",
    response_model=SettlementDetailsResponse
)
async def get_settlement_details(
    settlement_id: str,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Settlement).where(
            Settlement.settlement_id == settlement_id
        )
    )
 
    settlement = result.scalar_one_or_none()
 
    if not settlement:
        return {
            "message": "Settlement not found"
        }
 
    return {
        "settlement": settlement,
 
        "revenue_split": {
 
            "merchant_share":
                settlement.net_payout,
 
            "platform_fees":
                settlement.platform_fees,
 
            "discounts":
                settlement.discounts,
 
            "merchant_share_percentage":
                settlement.merchant_share_percentage,
 
            "platform_fee_percentage":
                settlement.platform_fee_percentage,
 
            "discount_percentage":
                settlement.discount_percentage
        },
 
        "service_fees": [
 
            {
                "service_name": "Platform Fee",
                "amount": settlement.platform_fees
            },
 
            {
                "service_name": "Delivery Commission",
                "amount": 84
            },
 
            {
                "service_name": "Payment Gateway Fee",
                "amount": 150.00
            }
        ]
    }
 
 
# ======================================================
# SCREEN 2
# EXPORT REPORT
# ======================================================
 
@router.get(
    "/settlements/{settlement_id}/report"
)
async def export_settlement_report(
    settlement_id: str,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(Settlement).where(
            Settlement.settlement_id == settlement_id
        )
    )
 
    settlement = result.scalar_one_or_none()
 
    if not settlement:
        return {
            "message": "Settlement not found"
        }
 
    output = StringIO()
 
    writer = csv.writer(output)
 
    writer.writerow([
        "Settlement Report"
    ])
 
    writer.writerow([
        "Settlement ID",
        settlement.settlement_id
    ])
 
    writer.writerow([
        "Cycle",
        settlement.cycle
    ])
 
    writer.writerow([
        "Gross Sales",
        settlement.gross_sales
    ])
 
    writer.writerow([
        "Deductions",
        settlement.deductions
    ])
 
    writer.writerow([
        "Net Payout",
        settlement.net_payout
    ])
 
    output.seek(0)
 
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename={settlement_id}.csv"
        }
    )
   
 
 
@router.get(
    "/tax-invoices",
    response_model=TaxInvoiceListResponse
)
async def get_tax_invoices(
    financial_year: str = "FY 2023-24",
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(TaxInvoice)
    )
 
    invoices = result.scalars().all()
 
    total_tds = sum(
        invoice.tds_amount
        for invoice in invoices
    )
 
    total_gst = sum(
        invoice.gst_amount
        for invoice in invoices
    )
 
    return {
        "financial_year": financial_year,
 
        "total_tds_withheld": total_tds,
 
        "net_gst_claimable": total_gst,
 
        "invoice_count": len(invoices),
 
        "invoices": invoices
    }
 
 
 
@router.get(
    "/tax-invoices/{invoice_id}"
)
async def download_tax_invoice(
    invoice_id: str,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(TaxInvoice).where(
            TaxInvoice.invoice_id == invoice_id
        )
    )
 
    invoice = result.scalar_one_or_none()
 
    if not invoice:
        return {
            "message": "Invoice not found"
        }
 
    return {
        "invoice_id": invoice.invoice_id,
        "month": invoice.month,
        "gst_amount": invoice.gst_amount,
        "tds_amount": invoice.tds_amount,
        "total_amount": invoice.total_amount,
        "invoice_type": invoice.invoice_type
    }
 
 
 
@router.get(
    "/tax-invoices/export/csv"
)
async def export_tax_invoice_csv(
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(TaxInvoice)
    )
 
    invoices = result.scalars().all()
 
    output = StringIO()
 
    writer = csv.writer(output)
 
    writer.writerow([
        "Invoice ID",
        "Month",
        "Invoice Type",
        "GST Amount",
        "TDS Amount",
        "Total Amount"
    ])
 
    for invoice in invoices:
 
        writer.writerow([
            invoice.invoice_id,
            invoice.month,
            invoice.invoice_type,
            invoice.gst_amount,
            invoice.tds_amount,
            invoice.total_amount
        ])
 
    output.seek(0)
 
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=tax_invoices.csv"
        }
    )
 
 
 
 
@router.post(
    "/tax-invoices/email-all"
)
async def email_all_tax_invoices():
 
    return {
        "message":
        "All tax invoices emailed successfully"
    }
 
 
 
@router.get(
    "/tax-invoices/export/zip"
)
async def download_tax_zip():
 
    return {
        "message":
        "FY ZIP export generated successfully"
    }
   
     
@router.get(
    "/bank-transfers",
    response_model=BankTransferResponse
)
async def get_bank_transfers(
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(BankTransfer)
    )
 
    transfers = result.scalars().all()
 
    total_amount = sum(
        transfer.amount
        for transfer in transfers
    )
 
    growth_percentage = 12
 
    receiving_account = {
        "bank_name":
            "Metropolitan Commercial Bank",
 
        "account_number":
            "**** **** 8291",
 
        "routing_number":
            "**** **442",
 
        "account_type":
            "Business Checking"
    }
 
    return {
        "mtd_settlement_amount": total_amount,
 
        "growth_percentage": growth_percentage,
 
        "receiving_account": receiving_account,
 
        "recent_transfers": transfers
    }
 
 
 
@router.get(
    "/bank-transfers/{transfer_reference}"
)
async def get_single_transfer(
    transfer_reference: str,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(BankTransfer).where(
            BankTransfer.transfer_reference
            == transfer_reference
        )
    )
 
    transfer = result.scalar_one_or_none()
 
    if not transfer:
        return {
            "message": "Transfer not found"
        }
 
    return transfer
 
 
 
@router.get(
    "/bank-transfers/export/csv"
)
async def export_bank_transfer_csv(
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(BankTransfer)
    )
 
    transfers = result.scalars().all()
 
    output = StringIO()
 
    writer = csv.writer(output)
 
    writer.writerow([
        "Reference",
        "Amount",
        "Status",
        "Date",
        "Time"
    ])
 
    for transfer in transfers:
 
        writer.writerow([
            transfer.transfer_reference,
            transfer.amount,
            transfer.transfer_status,
            transfer.transfer_date,
            transfer.transfer_time
        ])
 
    output.seek(0)
 
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=bank_transfers.csv"
        }
    )
 
 
 
 
@router.put(
    "/bank-transfers/account/update"
)
async def update_bank_account():
 
    return {
        "message":
        "Bank details updated successfully"
    }
 
 
# =====================================================
# TRANSFER ISSUES
# =====================================================
 
@router.get(
    "/bank-transfers/issues"
)
async def transfer_issues():
 
    return {
        "issues": [
            {
                "id": 1,
                "message":
                "Transfer delayed due to bank holiday"
            }
        ]
    }
   
   
# =====================================================
# REFUND & DEDUCTION TRACKING
# =====================================================
 
@router.get(
    "/refund-deductions",
    response_model=RefundDeductionResponse
)
async def get_refund_deductions(
    search: str = Query(default=None),
    category: str = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
 
    query = select(RefundDeduction)
 
    if search:
 
        query = query.where(
            RefundDeduction.order_id.ilike(
                f"%{search}%"
            )
        )
 
    if category:
 
        query = query.where(
            RefundDeduction.category == category
        )
 
    result = await db.execute(query)
 
    deductions = result.scalars().all()
 
    total_deductions = sum(
        item.deduction_amount
        for item in deductions
    )
 
    customer_refunds = sum(
        item.deduction_amount
        for item in deductions
        if item.category == "Customer Refund"
    )
 
    penalty_fees = sum(
        item.deduction_amount
        for item in deductions
        if item.category == "Penalty Fee"
    )
 
    return {
        "total_deductions": total_deductions,
 
        "customer_refunds": customer_refunds,
 
        "penalty_fees": penalty_fees,
 
        "dispute_success_rate": 68.5,
 
        "total_active_cases": 24,
 
        "total_pending_cases": 8,
 
        "deductions": deductions
    }
 
 
# =====================================================
# SINGLE REFUND/DEDUCTION
# =====================================================
 
@router.get(
    "/refund-deductions/{order_id}"
)
async def get_single_refund_deduction(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RefundDeduction).where(
            RefundDeduction.order_id == order_id
        )
    )
 
    deduction = result.scalar_one_or_none()
 
    if not deduction:
 
        return {
            "message":
            "Deduction record not found"
        }
 
    return deduction
 
 
# =====================================================
# EXPORT CSV
# =====================================================
 
@router.get(
    "/refund-deductions/export/csv"
)
async def export_refund_deduction_csv(
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RefundDeduction)
    )
 
    deductions = result.scalars().all()
 
    output = StringIO()
 
    writer = csv.writer(output)
 
    writer.writerow([
        "Order ID",
        "Category",
        "Reason",
        "Amount",
        "Status",
        "Risk Level"
    ])
 
    for item in deductions:
 
        writer.writerow([
            item.order_id,
            item.category,
            item.reason,
            item.deduction_amount,
            item.refund_status,
            item.risk_level
        ])
 
    output.seek(0)
 
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=refund_deductions.csv"
        }
    )
 
 
# =====================================================
# CUSTOMER REFUNDS ONLY
# =====================================================
 
@router.get(
    "/refund-deductions/customer-refunds"
)
async def get_customer_refunds(
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RefundDeduction).where(
            RefundDeduction.category
            == "Customer Refund"
        )
    )
 
    refunds = result.scalars().all()
 
    return refunds
 
 
# =====================================================
# PENALTY FEES ONLY
# =====================================================
 
@router.get(
    "/refund-deductions/penalty-fees"
)
async def get_penalty_fees(
    db: AsyncSession = Depends(get_db)
):
 
    result = await db.execute(
        select(RefundDeduction).where(
            RefundDeduction.category
            == "Penalty Fee"
        )
    )
 
    penalties = result.scalars().all()
 
    return penalties
 
 
# =====================================================
# SUPPORT
# =====================================================
 
@router.get(
    "/refund-deductions/support"
)
async def refund_support():
 
    return {
        "live_chat":
        "available",
 
        "email_support":
        "support@restaurant.com"
    }
 