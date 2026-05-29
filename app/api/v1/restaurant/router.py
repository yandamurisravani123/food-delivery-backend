from fastapi import APIRouter, Depends
from fastapi import UploadFile, File, Form
import os
from uuid import UUID
import shutil
from app.config.database import get_db
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.schemas.restaurant_bank import RestaurantBankRequest
from sqlalchemy import select, update
from sqlalchemy import Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.restaurant import InventoryAdjustment
from fastapi import HTTPException

from app.models.restaurant import (
    Ingredient,
    IngredientWaste,
    MenuIngredient,
    InventoryAdjustment
)

router = APIRouter(prefix="/restaurants",tags=["Restaurants"])

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

    restaurant_id: UUID = Form(...),

    item_name: str = Form(...),

    description: str = Form(...),

    category: str = Form(...),

    base_price: str = Form(...),

    tags: str = Form(None),

    tax_rate: str = Form(...),

    track_stock: bool = Form(True),

    combo_available: bool = Form(False),

    food_image: UploadFile | None = File(default=None),

    db: AsyncSession = Depends(get_db)
):

    try:

        UPLOAD_DIR = "uploads/menu"

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        image_path = None

        if food_image and food_image.filename:

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
            "item_id": item.id
        }

    except Exception as e:

        await db.rollback()

        print("ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

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

    result = await db.execute(
        select(MenuItem).where(
            MenuItem.id == item_id
        )
    )
    item = result.scalar_one_or_none()

    if not item:
        return {
            "error": "Menu item not found"
        }

    await db.delete(item)

    await db.commit()

    return {
        "message": "Menu item deleted successfully"
    }








from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.restaurant import Ingredient, IngredientWaste

from app.schemas.restaurant import (
    IngredientCreate,
    IngredientOut,
    IngredientPriceUpdate,
    WasteCreate
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
        print("❌ CREATE INGREDIENT ERROR:")
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

# async def get_current_restaurant():
#     return {
#         "restaurant_id": "your-restaurant-id"
#     }

# async def get_current_restaurant():
#     return {
#         "restaurant_id": UUID("35a297ca-80d3-4978-b07b-0066a0b6a706")
#     }
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


from app.services.campaign_service import DashboardService

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

@router.get("/{campaign_id}")
async def get_campaign(campaign_id: UUID, db: AsyncSession = Depends(get_db)):
    ...

@router.get("/{campaign_id}", response_model=CampaignOut)
async def get_campaign(
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
    return campaign


@router.patch("/{campaign_id}")
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