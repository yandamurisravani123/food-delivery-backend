from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import uuid

from app.config.database import get_db
from app.models.delivery import DeliveryAgent
from app.models.Vehicle import Vehicle
from app.models.PayoutAccount import PayoutAccount
from app.services.delivery_service import DeliveryDashboardService
from app.services.delivery_service import DeliveryHomeService
from app.services.delivery_service import DeliveryAgentService

from app.models.delivery import (
    DeliveryAgent,
    DriverStats,
    DriverOrder,
    DriverShift,
    PeakHourBonus,
    EarningsBoost
)

router = APIRouter(prefix="/Driver", tags=["Driver"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def get_driver_by_delivery_id(db, delivery_agent_id):
    result = await db.execute(
        select(DeliveryAgent).where(DeliveryAgent.id == delivery_agent_id)
    )
    return result.scalar_one_or_none()


# ================= LICENSE =================
@router.post("/upload-license")
async def upload_license(
    delivery_agent_id: uuid.UUID = Form(...),
    license_front: UploadFile = File(None),
    license_back: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    driver = await get_driver_by_delivery_id(db, delivery_agent_id)

    if not driver:
        raise HTTPException(404, "Driver not found")

    async def save(file):
        if file and file.filename:
            path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{file.filename}"
            with open(path, "wb") as f:
                f.write(await file.read())
            return path
        return None

    driver.license_front_url = await save(license_front)
    driver.license_back_url = await save(license_back)
    driver.is_license_uploaded = True

    await db.commit()
    await db.refresh(driver)

    return {"message": "License uploaded"}


# ================= VERIFY LICENSE =================
@router.put("/submit-verification/{delivery_agent_id}")
async def submit_verification(delivery_agent_id: uuid.UUID, db: AsyncSession = Depends(get_db)):

    driver = await get_driver_by_delivery_id(db, delivery_agent_id)

    if not driver:
        raise HTTPException(404, "Driver not found")

    if not driver.license_front_url or not driver.license_back_url:
        raise HTTPException(400, "Upload both sides first")

    driver.license_status = "pending"

    await db.commit()

    return {"message": "Submitted for verification"}


# ================= VEHICLE =================
@router.post("/vehicle")
async def register_vehicle(
    delivery_agent_id: uuid.UUID = Form(...),
    vehicle_type: str = Form(...),
    registration_number: str = Form(...),
    rc_front: UploadFile = File(None),
    rc_back: UploadFile = File(None),
    insurance: UploadFile = File(None),
    vehicle_photo: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    driver = await get_driver_by_delivery_id(db, delivery_agent_id)

    if not driver:
        raise HTTPException(404, "Driver not found")

    async def save(file):
        if file and file.filename:
            path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{file.filename}"
            with open(path, "wb") as f:
                f.write(await file.read())
            return path
        return None

    vehicle = Vehicle(
        driver_id=driver.id,
        vehicle_type=vehicle_type,
        registration_number=registration_number,
        rc_front_url=await save(rc_front),
        rc_back_url=await save(rc_back),
        insurance_url=await save(insurance),
        vehicle_photo_url=await save(vehicle_photo),
        status="pending"
    )

    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)

    return {"message": "Vehicle uploaded"}


# ================= PAYOUT =================
@router.post("/payout")
async def save_payout(
    delivery_agent_id: uuid.UUID = Form(...),
    account_holder_name: str = Form(...),
    account_number: str = Form(...),
    ifsc_code: str = Form(...),
    upi_id: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    driver = await get_driver_by_delivery_id(db, delivery_agent_id)

    if not driver:
        raise HTTPException(404, "Driver not found")

    payout = PayoutAccount(
        driver_id=driver.id,
        account_holder_name=account_holder_name,
        account_number=account_number,
        ifsc_code=ifsc_code,
        upi_id=upi_id,
        is_verified=False
    )

    db.add(payout)
    await db.commit()

    return {"message": "Payout saved"}


# ================= VERIFY BANK =================
@router.put("/verify-bank/{delivery_agent_id}")
async def verify_bank(delivery_agent_id: uuid.UUID, db: AsyncSession = Depends(get_db)):

    driver = await get_driver_by_delivery_id(db, delivery_agent_id)

    result = await db.execute(
        select(PayoutAccount).where(PayoutAccount.driver_id == driver.id)
    )
    payout = result.scalar_one_or_none()

    if not payout:
        raise HTTPException(404, "Payout not found")

    payout.is_verified = True
    await db.commit()

    return {"message": "Bank verified"}


# ================= FINAL STATUS =================
@router.get("/status/{delivery_agent_id}")
async def get_status(delivery_agent_id: uuid.UUID, db: AsyncSession = Depends(get_db)):

    driver = await get_driver_by_delivery_id(db, delivery_agent_id)

    if not driver:
        raise HTTPException(404, "Driver not found")

    vehicle = (await db.execute(
        select(Vehicle).where(Vehicle.driver_id == driver.id)
    )).scalar_one_or_none()

    payout = (await db.execute(
        select(PayoutAccount).where(PayoutAccount.driver_id == driver.id)
    )).scalar_one_or_none()

    return {
        "license": driver.license_status,
        "vehicle": vehicle.status if vehicle else "pending",
        "bank": "approved" if payout and payout.is_verified else "pending",
        "final_status": get_overall_status(driver, vehicle, payout)
    }


def get_overall_status(driver, vehicle, payout):
    if (
        driver.license_status == "approved"
        and vehicle and vehicle.status == "approved"
        and payout and payout.is_verified
    ):
        return "approved"

    if (
        driver.license_status == "rejected"
        or (vehicle and vehicle.status == "rejected")
    ):
        return "rejected"

    return "in_progress"



@router.get("/dashboard/{delivery_agent_id}")
async def driver_dashboard(
    delivery_agent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    dashboard = await DeliveryDashboardService.get_dashboard(
        db,
        delivery_agent_id
    )

    if not dashboard:
        raise HTTPException(
            status_code=404,
            detail="Delivery Agent not found"
        )

    return dashboard


@router.get("/home/{delivery_agent_id}")
async def driver_home(
    delivery_agent_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await DeliveryHomeService.get_home(
        db,
        delivery_agent_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Delivery Agent not found"
        )

    return result


@router.get("/break/status/{delivery_agent_id}")
async def break_status(
    delivery_agent_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    return await DeliveryAgentService.break_status(
        session,
        delivery_agent_id
    )

@router.put("/availability/{delivery_agent_id}")
async def save_availability_settings(
    delivery_agent_id: uuid.UUID,

    is_auto_accept: bool = Form(...),
    working_radius_km: int = Form(...),

    accept_cod: bool = Form(...),
    accept_bulk_orders: bool = Form(...),
    accept_fragile_items: bool = Form(...),
    accept_long_distance: bool = Form(...),

    vehicle_mode: str = Form(...),

    session: AsyncSession = Depends(get_db)
):

    return await DeliveryAgentService.save_availability_settings(
        session,
        delivery_agent_id,
        {
            "is_auto_accept": is_auto_accept,
            "working_radius_km": working_radius_km,
            "accept_cod": accept_cod,
            "accept_bulk_orders": accept_bulk_orders,
            "accept_fragile_items": accept_fragile_items,
            "accept_long_distance": accept_long_distance,
            "vehicle_mode": vehicle_mode
        }
    )


@router.get("/availability/{delivery_agent_id}")
async def get_availability_settings(
    delivery_agent_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):

    return await DeliveryAgentService.get_availability_settings(
        session,
        delivery_agent_id
    )