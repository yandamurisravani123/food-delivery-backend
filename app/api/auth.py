import os
import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    RegisterResponse,
    RegisterSuperAdmin,
    ResetPasswordRequest,
    TokenResponse,
    VerifyOtpRequest,
)
from app.schemas.delivery import (
    DeliveryAgentRegisterRequest,
    DeliveryAgentRegisterResponse,
    MessageResponse,
)
from app.schemas.restaurant import (
    RestaurantRegisterRequest,
    RestaurantRegisterResponse,
)
from app.services.auth_service import AuthService
from app.services.delivery_service import DeliveryAgentService
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/auth", tags=["Authentication"])

UPLOAD_DIR = "uploads/delivery_agents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

security = HTTPBearer()


@router.post("/register-Account", response_model=RegisterResponse)
async def register_account(
    payload: RegisterSuperAdmin,
    session: AsyncSession = Depends(get_db),
):
    return await AuthService.register_account(session, payload)


@router.post("/verify-otp", response_model=MessageResponse)
async def verify_otp(
    payload: VerifyOtpRequest,
    session: AsyncSession = Depends(get_db),
):
    return await AuthService.verify_otp(session, payload)


@router.post("/resend-otp", response_model=MessageResponse)
async def resend_otp(
    payload: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_db),
):
    return await AuthService.resend_otp(session, payload)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    return await AuthService.login(session, payload)


@router.post("/register", response_model=RestaurantRegisterResponse)
async def register_restaurant(
    payload: RestaurantRegisterRequest,
    session: AsyncSession = Depends(get_db),
):
    restaurant = await RestaurantService.register_restaurant(session, payload)
    return {
        "message": "Restaurant registered successfully. Waiting for super admin approval.",
        "restaurant_id": restaurant.id,
        "status": restaurant.status,
    }


@router.post("/Delivey-register", response_model=DeliveryAgentRegisterResponse)
async def register_delivery_agent(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    vehicle_type: str = Form(...),
    vehicle_number: str = Form(...),
    driving_license_number: str = Form(...),
    aadhaar_number: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),
    profile_image: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    file_extension = profile_image.filename.split(".")[-1] if "." in profile_image.filename else "jpg"
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await profile_image.read())

    payload = {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "password": password,
        "confirm_password": confirm_password,
        "vehicle_type": vehicle_type,
        "vehicle_number": vehicle_number,
        "driving_license_number": driving_license_number,
        "aadhaar_number": aadhaar_number,
        "city": city,
        "state": state,
        "pincode": pincode,
        "profile_image": file_path,
    }

    delivery_agent = await DeliveryAgentService.register(session, payload)

    return {
        "message": "Delivery agent registered successfully. Waiting for super admin approval.",
        "delivery_agent_id": delivery_agent.id,
        "status": delivery_agent.status,
    }


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    payload: ForgotPasswordRequest,
    session: AsyncSession = Depends(get_db),
):
    return await AuthService.forgot_password(session, payload)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    payload: ResetPasswordRequest,
    session: AsyncSession = Depends(get_db),
):
    return await AuthService.reset_password(session, payload)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    return await AuthService.logout(credentials.credentials)


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return current_user