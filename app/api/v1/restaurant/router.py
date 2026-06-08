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
from app.models import restaurant
from app.models.restaurant import Restaurant
<<<<<<< Updated upstream
from app.models.menu import MenuItem       
from app.schemas import order
from app.schemas.restaurant_bank import RestaurantBankRequest
=======
from app.models.menu import MenuItem
from app.schemas.restaurant import (
    RestaurantRegisterRequest,
    RestaurantOut,
    RestaurantApprovalResponse
)
>>>>>>> Stashed changes
from app.models.combo import MealCombo
from app.models.customization import (
    CustomizationGroup,
    CustomizationOption
)

from app.models.pricing_rule import PricingRule
from app.models.pricing_analytics import PricingAnalytics
from app.models.menu_schedule import MenuSchedule

<<<<<<< Updated upstream
from app.models.gallery import Gallery

from app.models.order import Order, OrderStatus
from app.models.order_items import OrderItems
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from app.services.analytics_service import (

    get_top_selling_by_quantity,

    get_top_selling_by_revenue,

    get_category_insights,
 
    get_menu_rankings,
 
    get_dashboard_data
)

from app.services.dashboard_service import DashboardService
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
 
=======
from app.models.gallery import FoodGallery
from sqlalchemy.ext.asyncio import AsyncSession
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    db.add(restaurant)

    db.commit()

    db.refresh(restaurant)
<<<<<<< HEAD
=======
    await db.commit()

    await db.refresh(restaurant)
>>>>>>> smart-bidding-feature
=======


@router.post("/restaurant-onboarding")
def save_restaurant(
    payload: RestaurantRegisterRequest,
    db: Session = Depends(get_db)
):
    #db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
>>>>>>> Stashed changes
=======
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c

    return {
        "message": "Restaurant onboarding saved",
        "restaurant_id": restaurant.id,
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

<<<<<<< Updated upstream
    # Async query fix
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    restaurant = result.scalars().first()

    if not restaurant:
        return {"error": "Restaurant not found"}

    UPLOAD_DIR = "uploads/documents"
<<<<<<< HEAD
=======
# @router.post("/register")
# async def register(data: RegisterSchema, db: AsyncSession = Depends(get_db)):
#     try:
#         # your code
#         return {"message": "success"}

#     except Exception as e:
#         print("ERROR:", e)
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/bank-details")
async def save_bank_details(
    payload: RestaurantBankRequest,
    db: AsyncSession = Depends(get_db)
=======
# @router.post("/bank-details")
# def save_bank_details(
#     payload: RestaurantBankRequest,vvv
#     db: Session = Depends(get_db)
# ):
@router.post("/bank-details")
def save_bank_details(

    restaurant_id: str = Form(...),h

    bank_account_holder: str = Form(...),

    bank_account_number: str = Form(...),

    confirm_account_number: str = Form(...),

    ifsc_code: str = Form(...),

    db: Session = Depends(get_db)

):

    if bank_account_number != confirm_account_number:
        return {
            "error": "Account numbers do not match"
        }

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        return {
            "error": "Restaurant not found"
        }

    restaurant.bank_account_holder = bank_account_holder
    restaurant.bank_account_number = bank_account_number
    restaurant.ifsc_code = ifsc_code

    db.commit()

    return {
        "message": "Bank details saved successfully"
    }
    
    if payload.bank_account_number != payload.confirm_account_number:
        return {
            "error": "Account numbers do not match"
        }

    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == payload.restaurant_id
        )
    )
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        return {
            "error": "Restaurant not found"
        }

    restaurant.bank_account_holder = payload.bank_account_holder

    restaurant.bank_account_number = payload.bank_account_number

    restaurant.ifsc_code = payload.ifsc_code

    await db.commit()

    return {
        "message": "Bank details saved successfully"
    }
    
@router.post("/documents")
async def upload_restaurant_documents(

    restaurant_id: str = Form(...),

    gst_certificate: UploadFile = File(None),

    fssai_license_file: UploadFile = File(None),

    cancelled_cheque: UploadFile = File(None),

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == restaurant_id
        )
    )

    restaurant = result.scalar_one_or_none()
    if not restaurant:
        return {
            "error": "Restaurant not found"
        }

    UPLOAD_DIR = "uploads/documents"

>>>>>>> smart-bidding-feature
=======
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c
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
def add_menu_item(

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

    db.commit()

    db.refresh(item)

    return {
        "message": "Menu item added successfully",
        "item_id": item.id
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

        item = MenuItem(
            restaurant_id=restaurant_id,
            item_name=row.get("item_name", ""),
            description=row.get("description", ""),
            category=row.get("category", ""),
            base_price=float(row.get("base_price", 0)),
            tags=row.get("tags", ""),
            tax_rate=row.get("tax_rate", "0"),
            track_stock=str(row.get("track_stock", "false")).lower() == "true",
            combo_available=str(row.get("combo_available", "false")).lower() == "true"
        )

        db.add(item)
        created_items.append(row.get("item_name"))

    await db.commit()

    return {
        "message": "Menu items uploaded successfully",
        "total_items": len(created_items),
        "items": created_items
    }
    
@router.get("/menu/{restaurant_id}")
async def get_restaurant_menu(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id)
    )

    items = result.scalars().all()

    return {
        "restaurant_id": restaurant_id,
        "total_items": len(items),
        "menu": items
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

    result_list = []

    for o in orders:
        result_list.append({
            "id": o.id,

            
            "items": [
                {
                    "name": item.name,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in o.items
            ] if o.items else [],

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
        })

    return result_list

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

    items = [
        {
            "name": item.name,
            "quantity": item.quantity,
            "price": item.price
        }
        for item in order.items
    ] if order.items else []

    subtotal = sum(i["price"] * i["quantity"] for i in items)
    delivery_fee = order.delivery_fee or 0
    tax = subtotal * (order.tax_percent / 100)
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
        select(Order).where(
            Order.restaurant_id == restaurant_id,
            cast(Order.id, String).like(f"%{query}%")
        )
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
<<<<<<< HEAD
    db: AsyncSession = Depends(get_db)):
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


# from app.models.campaign import Campaign, FlashOffer, OfferControl

# @router.post("/campaign/{campaign_id}/join")
# async def join_campaign(campaign_id: UUID, db: AsyncSession = Depends(get_db)):

#     result = await db.execute(
#         update(Campaign)
#         .where(Campaign.id == campaign_id)
#         .values(reach_count=Campaign.reach_count + 1)
#         .returning(Campaign.id)
#     )

#     updated = result.fetchone()

#     if not updated:
#         raise HTTPException(status_code=404, detail="Campaign not found")

#     await db.commit()

#     return {
#         "message": "Joined campaign successfully",
#         "campaign_id": updated.id}

# @router.post("/flash-offer/{offer_id}/activate")
# async def activate_flash_offer(offer_id: UUID, db: AsyncSession = Depends(get_db)):

#     result = await db.execute(
#         select(FlashOffer).where(FlashOffer.id == offer_id)
#     )

#     flash_offer = result.scalar_one_or_none()

#     if not flash_offer:
#         raise HTTPException(status_code=404, detail="Flash offer not found")

#     flash_offer.is_active = True

#     await db.commit()

#     return {"message": "Flash offer activated"}

# @router.put("/offer-control")
# async def update_offer_control(
#     auto_apply: bool,
#     minimum_discount: float,
#     db: AsyncSession = Depends(get_db)
# ):

#     result = await db.execute(
#         select(OfferControl)
#     )

#     control = result.scalars().first()

#     if not control:

#         control = OfferControl(
#             auto_apply=auto_apply,
#             minimum_discount=minimum_discount
#         )

#         db.add(control)

#     else:

#         control.auto_apply = auto_apply
#         control.minimum_discount = minimum_discount

#     await db.commit()

#     return {
#         "message": "Offer control updated"
#     }
from sqlalchemy import text
from app.models.campaign import Campaign
@router.put("/campaign/{campaign_id}/smart-bidding")
async def toggle_smart_bidding(
    campaign_id: UUID,
>>>>>>> smart-bidding-feature
=======
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c
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
            "status": order.status,
        }
<<<<<<< HEAD

        select(Campaign).where(Campaign.id == campaign_id)
    )

    campaign = result.scalar_one_or_none()

=======
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c
    }


@router.put("/campaign/{campaign_id}/smart-bidding")
async def toggle_smart_bidding(
    campaign_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id)
    )
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found",
        )

    campaign.smart_bidding = not campaign.smart_bidding

    await db.commit()
    await db.refresh(campaign)

    return {
        "message": "Smart bidding updated",
        "smart_bidding": campaign.smart_bidding,
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