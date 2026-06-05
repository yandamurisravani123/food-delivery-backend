from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile, File, Form
import csv
import io
import uuid

try:
    import pandas as pd
    _pandas_available = True
except ImportError:
    _pandas_available = False
import os
import shutil
from app.config.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem
from app.schemas.restaurant_bank import RestaurantBankRequest
from app.models.combo import MealCombo
from app.models.customization import (
    CustomizationGroup,
    CustomizationOption
)

from app.models.pricing_rule import PricingRule
from app.models.pricing_analytics import PricingAnalytics
from app.models.menu_schedule import MenuSchedule

from app.models.gallery import FoodGallery

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


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
        "restaurant_id": str(restaurant.id),
        "logo": logo_filename
    }


@router.post("/bank-details")
async def save_bank_details(
    payload: RestaurantBankRequest,
    db: AsyncSession = Depends(get_db)
):

    if payload.bank_account_number != payload.confirm_account_number:
        return {
            "error": "Account numbers do not match"
        }

    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(payload.restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {payload.restaurant_id}"
        )

    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == restaurant_uuid
        )
    )

    restaurant = result.scalar_one_or_none()

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

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
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == restaurant_uuid
        )
    )

    restaurant = result.scalar_one_or_none()

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

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
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == restaurant_uuid
        )
    )

    restaurant = result.scalar_one_or_none()

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    UPLOAD_DIR = "uploads/menu"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    image_path = None

    if food_image:

        image_path = f"{UPLOAD_DIR}/{food_image.filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(food_image.file, buffer)

    item = MenuItem(

        restaurant_id=restaurant_uuid,

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
    
@router.post("/menu/bulk-upload")
async def bulk_upload_menu(

    restaurant_id: str = Form(...),

    file: UploadFile = File(...),

    db: AsyncSession = Depends(get_db)
):
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    result = await db.execute(
        select(Restaurant).where(
            Restaurant.id == restaurant_uuid
        )
    )

    restaurant = result.scalar_one_or_none()

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    if not file.filename.endswith(".csv"):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )

    temp_file = f"uploads/{file.filename}"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    created_items = []

    if _pandas_available:
        df = pd.read_csv(temp_file)
        rows = [row for _, row in df.iterrows()]
    else:
        with open(temp_file, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

    for row in rows:

        item = MenuItem(

            restaurant_id=restaurant_uuid,

            item_name=row["item_name"],

            description=row["description"],

            category=row["category"],

            base_price=float(row["base_price"]),

            tags=row["tags"],

            tax_rate=row["tax_rate"],

            track_stock=bool(row["track_stock"]),

            combo_available=bool(row["combo_available"])
        )

        db.add(item)

        created_items.append(row["item_name"])

    db.commit()

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
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    result = await db.execute(
        select(MenuItem).where(
            MenuItem.restaurant_id == restaurant_uuid
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

    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

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

    result = await db.execute(
        select(MenuItem).where(
            MenuItem.id == item_id
        )
    )

    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    await db.delete(item)

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
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    UPLOAD_DIR = "uploads/combos"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    image_path = None

    if combo_image:

        image_path = f"{UPLOAD_DIR}/{combo_image.filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(combo_image.file, buffer)

    combo = MealCombo(

        restaurant_id=restaurant_uuid,

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
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    result = await db.execute(
        select(MealCombo).where(
            MealCombo.restaurant_id == restaurant_uuid
        )
    )

    return result.scalars().all()

@router.delete("/combos/{combo_id}")
async def delete_combo(
    combo_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MealCombo).where(
            MealCombo.id == combo_id
        )
    )

    combo = result.scalar_one_or_none()

    if not combo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Combo not found"
        )

    await db.delete(combo)

    await db.commit()

    return {
        "message": "Combo deleted successfully"
    }
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
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    result = await db.execute(
        select(CustomizationGroup).where(
            CustomizationGroup.restaurant_id == restaurant_uuid
        )
    )

    groups = result.scalars().all()

    result_list = []

    for group in groups:

        options_result = await db.execute(
            select(CustomizationOption).where(
                CustomizationOption.group_id == group.id
            )
        )

        options = options_result.scalars().all()

        result_list.append({

            "group_id": group.id,

            "group_name": group.group_name,

            "options": options
        })

    return result_list

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

        "increase_percentage": analytics.increase_percentage
    }


@router.put("/menu/item/{item_id}/pricing")
async def update_menu_pricing(

    item_id: str,

    base_price: float,

    tax_category: str,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(MenuItem).where(
            MenuItem.id == item_id
        )
    )

    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    item.base_price = base_price

    item.tax_category = tax_category

    await db.commit()

    return {
        "message": "Pricing updated successfully"
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

    return result.scalars().all()

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

    rule = result.scalar_one_or_none()

    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing rule not found"
        )

    await db.delete(rule)

    await db.commit()

    return {
        "message": "Pricing rule deleted"
    }

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

    return result.scalars().all()

@router.post("/gallery/upload")
async def upload_gallery_images(

    restaurant_id: str = Form(...),

    images: list[UploadFile] = File(...),

    db: AsyncSession = Depends(get_db)
):
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    UPLOAD_DIR = "uploads/gallery"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    uploaded_images = []

    for image in images:

        image_path = f"{UPLOAD_DIR}/{image.filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        gallery = FoodGallery(

            restaurant_id=restaurant_uuid,

            image_url=image_path,

            status="unassigned"
        )

        db.add(gallery)

        uploaded_images.append(image.filename)

    await db.commit()

    return {
        "message": "Images uploaded successfully",
        "files": uploaded_images
    }
    
@router.get("/gallery/{restaurant_id}")
async def get_gallery_images(
    restaurant_id: str,
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    # Validate and convert restaurant_id to UUID
    try:
        restaurant_uuid = uuid.UUID(restaurant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid restaurant ID format: {restaurant_id}"
        )

    offset = (page - 1) * limit

    result = await db.execute(
        select(FoodGallery).where(
            FoodGallery.restaurant_id == restaurant_uuid
        ).offset(offset).limit(limit)
    )

    images = result.scalars().all()

    result_list = []

    for image in images:

        result_list.append({

            "id": str(image.id),

            "image_url": image.image_url,

            "status": image.status,

            "menu_item_id": image.menu_item_id
        })

    return result_list

@router.put("/gallery/assign")
async def assign_image_to_menu(

    gallery_id: str,

    menu_item_id: str,

    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(FoodGallery).where(
            FoodGallery.id == gallery_id
        )
    )

    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    image.menu_item_id = menu_item_id

    image.status = "assigned"

    await db.commit()

    return {
        "message": "Image assigned successfully"
    }
    
@router.put("/gallery/unassign/{gallery_id}")
async def unassign_gallery_image(
    gallery_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(FoodGallery).where(
            FoodGallery.id == gallery_id
        )
    )

    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    image.menu_item_id = None

    image.status = "unassigned"

    await db.commit()

    return {
        "message": "Image unassigned"
    }

@router.delete("/gallery/{gallery_id}")
async def delete_gallery_image(
    gallery_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(FoodGallery).where(
            FoodGallery.id == gallery_id
        )
    )

    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )

    await db.delete(image)

    await db.commit()

    return {
        "message": "Image deleted successfully"
    }