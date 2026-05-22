from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
from fastapi import UploadFile, File, Form
import os
import shutil
from app.config.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
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

    db: Session = Depends(get_db)
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
        "restaurant_id": restaurant.id,
        "logo": logo_filename
    }


@router.post("/bank-details")
def save_bank_details(
    payload: RestaurantBankRequest,
    db: Session = Depends(get_db)
):

    if payload.bank_account_number != payload.confirm_account_number:
        return {
            "error": "Account numbers do not match"
        }

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == payload.restaurant_id
    ).first()

    if not restaurant:
        return {
            "error": "Restaurant not found"
        }

    restaurant.bank_account_holder = payload.bank_account_holder

    restaurant.bank_account_number = payload.bank_account_number

    restaurant.ifsc_code = payload.ifsc_code

    db.commit()

    return {
        "message": "Bank details saved successfully"
    }
    
@router.post("/documents")
def upload_restaurant_documents(

    restaurant_id: str = Form(...),

    gst_certificate: UploadFile = File(None),

    fssai_license_file: UploadFile = File(None),

    cancelled_cheque: UploadFile = File(None),

    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        return {
            "error": "Restaurant not found"
        }

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

    db.commit()

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

    db: Session = Depends(get_db)
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
def bulk_upload_menu(

    restaurant_id: str = Form(...),

    file: UploadFile = File(...),

    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".csv"):

        return {
            "error": "Only CSV files are allowed"
        }

    temp_file = f"uploads/{file.filename}"

    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(temp_file)

    created_items = []

    for _, row in df.iterrows():

        item = MenuItem(

            restaurant_id=restaurant_id,

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
def get_restaurant_menu(
    restaurant_id: str,
    db: Session = Depends(get_db)
):

    items = db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id
    ).all()

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
def update_stock_status(
    item_id: str,
    is_available: bool,
    db: Session = Depends(get_db)
):

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        return {
            "error": "Menu item not found"
        }

    item.is_available = is_available

    db.commit()

    return {
        "message": "Stock updated successfully"
    }
    
@router.put("/menu/item/{item_id}/stock")
def update_stock_status(
    item_id: str,
    is_available: bool,
    db: Session = Depends(get_db)
):

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        return {
            "error": "Menu item not found"
        }

    item.is_available = is_available

    db.commit()

    return {
        "message": "Stock updated successfully"
    }
    
@router.delete("/menu/item/{item_id}")
def delete_menu_item(
    item_id: str,
    db: Session = Depends(get_db)
):

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        return {
            "error": "Menu item not found"
        }

    db.delete(item)

    db.commit()

    return {
        "message": "Menu item deleted successfully"
    }
    
@router.post("/combos")
def create_meal_combo(

    restaurant_id: str = Form(...),

    combo_name: str = Form(...),

    description: str = Form(...),

    combo_price: float = Form(...),

    tags: str = Form(None),

    combo_image: UploadFile = File(None),

    db: Session = Depends(get_db)
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

    db.commit()

    db.refresh(combo)

    return {
        "message": "Meal combo created successfully",
        "combo_id": combo.id
    }
@router.get("/combos/{restaurant_id}")
def get_combos(
    restaurant_id: str,
    db: Session = Depends(get_db)
):

    combos = db.query(MealCombo).filter(
        MealCombo.restaurant_id == restaurant_id
    ).all()

    return combos
@router.delete("/combos/{combo_id}")

def delete_combo(
    combo_id: str,
    db: Session = Depends(get_db)
):

    combo = db.query(MealCombo).filter(
        MealCombo.id == combo_id
    ).first()

    if not combo:
        return {
            "error": "Combo not found"
        }

    db.delete(combo)

    db.commit()

    return {
        "message": "Combo deleted successfully"
    }
@router.post("/customization-groups")
def create_customization_group(

    restaurant_id: str,

    group_name: str,

    db: Session = Depends(get_db)
):

    group = CustomizationGroup(

        restaurant_id=restaurant_id,

        group_name=group_name
    )

    db.add(group)

    db.commit()

    db.refresh(group)

    return {
        "message": "Customization group created",
        "group_id": group.id
    }
@router.post("/customization-options")
def create_customization_option(

    group_id: str,

    option_name: str,

    extra_price: float,

    db: Session = Depends(get_db)
):

    option = CustomizationOption(

        group_id=group_id,

        option_name=option_name,

        extra_price=extra_price
    )

    db.add(option)

    db.commit()

    db.refresh(option)

    return {
        "message": "Option added successfully",
        "option_id": option.id
    }
@router.get("/customization-groups/{restaurant_id}")
def get_customization_groups(
    restaurant_id: str,
    db: Session = Depends(get_db)
):

    groups = db.query(CustomizationGroup).filter(
        CustomizationGroup.restaurant_id == restaurant_id
    ).all()

    result = []

    for group in groups:

        options = db.query(CustomizationOption).filter(
            CustomizationOption.group_id == group.id
        ).all()

        result.append({

            "group_id": group.id,

            "group_name": group.group_name,

            "options": options
        })

    return result

@router.post("/pricing-analytics")
def create_pricing_analytics(

    restaurant_id: str,

    increase_percentage: float,

    message: str,

    db: Session = Depends(get_db)
):

    analytics = PricingAnalytics(

        restaurant_id=restaurant_id,

        increase_percentage=increase_percentage,

        message=message
    )

    db.add(analytics)

    db.commit()

    db.refresh(analytics)

    return {

        "message": "Pricing analytics created successfully",

        "analytics_id": analytics.id,

        "increase_percentage": analytics.increase_percentage
    }


@router.put("/menu/item/{item_id}/pricing")
def update_menu_pricing(

    item_id: str,

    base_price: float,

    tax_category: str,

    db: Session = Depends(get_db)
):

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        return {
            "error": "Menu item not found"
        }

    item.base_price = base_price

    item.tax_category = tax_category

    db.commit()

    return {
        "message": "Pricing updated successfully"
    }

@router.post("/pricing-rules")
def create_pricing_rule(

    menu_item_id: str,

    rule_name: str,

    adjustment_type: str,

    adjustment_value: float,

    start_date: str,

    end_date: str,

    active_days: str = None,

    db: Session = Depends(get_db)
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

    db.commit()

    db.refresh(rule)

    return {
        "message": "Pricing rule created",
        "rule_id": rule.id
    }

@router.get("/pricing-rules/{menu_item_id}")
def get_pricing_rules(
    menu_item_id: str,
    db: Session = Depends(get_db)
):

    rules = db.query(PricingRule).filter(
        PricingRule.menu_item_id == menu_item_id
    ).all()

    return rules

@router.delete("/pricing-rules/{rule_id}")
def delete_pricing_rule(
    rule_id: str,
    db: Session = Depends(get_db)
):

    rule = db.query(PricingRule).filter(
        PricingRule.id == rule_id
    ).first()

    if not rule:
        return {
            "error": "Pricing rule not found"
        }

    db.delete(rule)

    db.commit()

    return {
        "message": "Pricing rule deleted"
    }

@router.post("/menu-schedule")
def create_menu_schedule(

    menu_item_id: str,

    day_of_week: str,

    start_time: str,

    end_time: str,

    service_name: str,

    db: Session = Depends(get_db)
):

    schedule = MenuSchedule(

        menu_item_id=menu_item_id,

        day_of_week=day_of_week,

        start_time=start_time,

        end_time=end_time,

        service_name=service_name
    )

    db.add(schedule)

    db.commit()

    db.refresh(schedule)

    return {
        "message": "Schedule created",
        "schedule_id": schedule.id
    }

@router.get("/menu-schedule/{menu_item_id}")
def get_menu_schedule(
    menu_item_id: str,
    db: Session = Depends(get_db)
):

    schedules = db.query(MenuSchedule).filter(
        MenuSchedule.menu_item_id == menu_item_id
    ).all()

    return schedules

@router.post("/gallery/upload")
def upload_gallery_images(

    restaurant_id: str = Form(...),

    images: list[UploadFile] = File(...),

    db: Session = Depends(get_db)
):

    UPLOAD_DIR = "uploads/gallery"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    uploaded_images = []

    for image in images:

        image_path = f"{UPLOAD_DIR}/{image.filename}"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        gallery = FoodGallery(

            restaurant_id=restaurant_id,

            image_url=image_path,

            status="unassigned"
        )

        db.add(gallery)

        uploaded_images.append(image.filename)

    db.commit()

    return {
        "message": "Images uploaded successfully",
        "files": uploaded_images
    }
    
@router.get("/gallery/{restaurant_id}")
def get_gallery_images(
    restaurant_id: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    offset = (page - 1) * limit

    images = db.query(FoodGallery).filter(
        FoodGallery.restaurant_id == restaurant_id
    ).offset(offset).limit(limit).all()

    result = []

    for image in images:

        result.append({

            "id": str(image.id),

            "image_url": image.image_url,

            "status": image.status,

            "menu_item_id": image.menu_item_id
        })

    return result

@router.put("/gallery/assign")
def assign_image_to_menu(

    gallery_id: str,

    menu_item_id: str,

    db: Session = Depends(get_db)
):

    image = db.query(FoodGallery).filter(
        FoodGallery.id == gallery_id
    ).first()

    if not image:
        return {
            "error": "Image not found"
        }

    image.menu_item_id = menu_item_id

    image.status = "assigned"

    db.commit()

    return {
        "message": "Image assigned successfully"
    }
    
@router.put("/gallery/unassign/{gallery_id}")
def unassign_gallery_image(
    gallery_id: str,
    db: Session = Depends(get_db)
):

    image = db.query(FoodGallery).filter(
        FoodGallery.id == gallery_id
    ).first()

    if not image:
        return {
            "error": "Image not found"
        }

    image.menu_item_id = None

    image.status = "unassigned"

    db.commit()

    return {
        "message": "Image unassigned"
    }

@router.delete("/gallery/{gallery_id}")
def delete_gallery_image(
    gallery_id: str,
    db: Session = Depends(get_db)
):

    image = db.query(FoodGallery).filter(
        FoodGallery.id == gallery_id
    ).first()

    if not image:
        return {
            "error": "Image not found"
        }

    db.delete(image)

    db.commit()

    return {
        "message": "Image deleted successfully"
    }