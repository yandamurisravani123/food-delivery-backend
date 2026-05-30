from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import pandas as pd
import os
import shutil

from app.config.database import get_db

from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.combo import MealCombo
from app.models.customization import (
    CustomizationGroup,
    CustomizationOption
)
from app.models.pricing_rule import PricingRule
from app.models.pricing_analytics import PricingAnalytics
from app.models.menu_schedule import MenuSchedule
from app.models.gallery import FoodGallery

from app.schemas.restaurant_bank import RestaurantBankRequest
from app.models.order import Order
from app.models.user import User

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)

# RESTAURANT ONBOARDING

@router.post("/onboarding")
async def restaurant_onboarding(

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

    await db.commit()

    await db.refresh(restaurant)

    return {
        "message": "Restaurant onboarding saved",
        "restaurant_id": restaurant.id,
        "logo": logo_filename
    }

# BANK DETAILS

@router.post("/bank-details")
async def save_bank_details(
    payload: RestaurantBankRequest,
    db: AsyncSession = Depends(get_db)
):

    if payload.bank_account_number != payload.confirm_account_number:
        return {
            "error": "Account numbers do not match"
        }

    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == payload.restaurant_id
        )
    )

    restaurant = result.scalars().first()

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

# DOCUMENT UPLOAD

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

    restaurant = result.scalars().first()

    if not restaurant:
        return {
            "error": "Restaurant not found"
        }

    UPLOAD_DIR = "uploads/documents"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if gst_certificate:

        gst_path = f"{UPLOAD_DIR}/{gst_certificate.filename}"

        with open(gst_path, "wb") as buffer:
            shutil.copyfileobj(gst_certificate.file, buffer)

        restaurant.gst_certificate = gst_path

    if fssai_license_file:

        fssai_path = f"{UPLOAD_DIR}/{fssai_license_file.filename}"

        with open(fssai_path, "wb") as buffer:
            shutil.copyfileobj(fssai_license_file.file, buffer)

        restaurant.fssai_license_file = fssai_path

    if cancelled_cheque:

        cheque_path = f"{UPLOAD_DIR}/{cancelled_cheque.filename}"

        with open(cheque_path, "wb") as buffer:
            shutil.copyfileobj(cancelled_cheque.file, buffer)

        restaurant.cancelled_cheque = cheque_path

    await db.commit()

    return {
        "message": "Documents uploaded successfully"
    }

# ADD MENU ITEM

from uuid import UUID
import uuid
import os
import shutil

from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

@router.post("/menu/add-item")
async def add_menu_item(
    restaurant_id: uuid.UUID = Form(...),

    item_name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),

    base_price: float = Form(...),

    tags: str | None = Form(None),

    tax_rate: float = Form(...),

    track_stock: bool = Form(True),

    combo_available: bool = Form(False),

    food_image: UploadFile | None = File(None),

    db: AsyncSession = Depends(get_db)
):

    try:
        UPLOAD_DIR = "uploads/menu"
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        image_path = None

        if food_image and food_image.filename:

            filename = f"{uuid.uuid4()}_{food_image.filename}"

            image_path = os.path.join(UPLOAD_DIR, filename)

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
            "item_id": item.id
        }

    except Exception as e:
        await db.rollback()

        return {
            "error": str(e)
        }
    
# GET MENU

@router.get("/menu/{restaurant_id}")
async def get_restaurant_menu(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MenuItem).where(
            MenuItem.restaurant_id == restaurant_id
        )
    )

    items = result.scalars().all()

    grouped_menu = {}

    for item in items:

        category = item.category or "Others"

        if category not in grouped_menu:
            grouped_menu[category] = []

        grouped_menu[category].append({
            "id": item.id,
            "item_name": item.item_name,
            "price": item.base_price,
            "available": item.is_available,
            "image": item.image_url
        })

    return grouped_menu

# UPDATE STOCK

@router.put("/menu/item/{item_id}/stock")
async def update_stock_status(
    item_id: str,
    is_available: bool,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MenuItem).where(
            MenuItem.id == item_id
        )
    )

    item = result.scalars().first()

    if not item:
        return {
            "error": "Menu item not found"
        }

    item.is_available = is_available

    await db.commit()

    return {
        "message": "Stock updated successfully"
    }

# DELETE MENU ITEM

@router.delete("/menu/item/{item_id}")
async def delete_menu_item(
    item_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MenuItem).where(
            MenuItem.id == item_id
        )
    )

    item = result.scalars().first()

    if not item:
        return {
            "error": "Menu item not found"
        }

    await db.delete(item)

    await db.commit()

    return {
        "message": "Menu item deleted successfully"
    }

# GET COMBOS

@router.get("/combos/{restaurant_id}")
async def get_combos(
    restaurant_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MealCombo).where(
            MealCombo.restaurant_id == restaurant_id
        )
    )

    combos = result.scalars().all()

    return combos

# CREATE COMBO

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


# ROUTER

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
            User.full_name,
            Order.total_amount,
            Order.visit_count
        )

        .join(User, User.id == Order.user_id)

        .where(Order.restaurant_id == restaurant_id)

        .order_by(Order.total_amount.desc())

        .limit(5)
    )

    customers = []

    for row in result.all():

        customers.append({

            "customer_name": row.full_name,

            "total_spend": row.total_amount,

            "visits": row.visit_count
        })

    return customers


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

  
        

    

   
 

   
     