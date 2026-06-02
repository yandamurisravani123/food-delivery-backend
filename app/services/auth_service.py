from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.config.security import (
    create_access_token,
    hash_password,
    token_fingerprint,
    verify_password,
)
from app.core.redis_client import redis_client
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    LoginRequest,
    MessageResponse,
    RegisterResponse,
    RegisterSuperAdmin,
    ResetPasswordRequest,
    TokenResponse,
    UserOut,
    VerifyOtpRequest,
)
from app.utils.email_utils import send_otp_email


class AuthService:
    @staticmethod
    async def register_account(session: AsyncSession, payload: RegisterSuperAdmin):
        if payload.password != payload.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password do not match",
            )

        existing = await AuthRepository.get_user_by_email(session, payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed = hash_password(payload.password)

        if payload.role == "super_admin":
            user = await AuthRepository.create_user(
                session=session,
                full_name=payload.full_name,
                email=payload.email,
                phone=payload.phone,
                hashed_password=hashed,
                role="super_admin",
                is_verified=True,
                is_active=True,
                is_super_admin=True,
            )

            return RegisterResponse(
                message="Super admin registered successfully.",
                user=UserOut(
                    id=user.id,
                    name=user.full_name,
                    email=user.email,
                    role=user.role,
                    status="active",
                    is_active=user.is_active,
                ),
            )

        user = await AuthRepository.create_user(
            session=session,
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
            hashed_password=hashed,
            role="user",
            is_verified=False,
            is_active=False,
            is_super_admin=False,
        )

        otp = f"{secrets.randbelow(1000000):06d}"
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        redis_key = f"otp:{payload.email.lower()}"
        await redis_client.setex(redis_key, 600, otp_hash)

        send_otp_email(payload.email, otp)

        return RegisterResponse(
            message="User registered successfully. OTP sent to email.",
            user=UserOut(
                id=user.id,
                name=user.full_name,
                email=user.email,
                role=user.role,
                status="inactive",
                is_active=user.is_active,
            ),
        )

    @staticmethod
    async def verify_otp(session: AsyncSession, payload: VerifyOtpRequest):
        user = await AuthRepository.get_user_by_email(session, payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        redis_key = f"otp:{payload.email.lower()}"
        stored_hash = await redis_client.get(redis_key)

        if not stored_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP expired or not found",
            )

        otp_hash = hashlib.sha256(payload.otp.encode()).hexdigest()
        if otp_hash != stored_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP",
            )

        user.is_verified = True
        user.is_active = True
        await session.commit()
        await session.refresh(user)

        await redis_client.delete(redis_key)

        return MessageResponse(message="OTP verified successfully")

    @staticmethod
    async def resend_otp(session: AsyncSession, payload: ForgotPasswordRequest):
        user = await AuthRepository.get_user_by_email(session, payload.email)
        if not user:
            return MessageResponse(message="If the email exists, OTP has been sent")

        if user.role != "user":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP verification is only for user role",
            )

        otp = f"{secrets.randbelow(1000000):06d}"
        otp_hash = hashlib.sha256(otp.encode()).hexdigest()

        await redis_client.setex(f"otp:{payload.email.lower()}", 600, otp_hash)

        send_otp_email(payload.email, otp)

        return MessageResponse(message="OTP resent successfully")

    @staticmethod
    async def login(session: AsyncSession, payload: LoginRequest):
        user = await AuthRepository.get_user_by_email(session, payload.email)
        if user:
            if not verify_password(payload.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            token = create_access_token(
                data={
                    "sub": str(user.id),
                    "email": user.email,
                    "role": user.role,
                    "entity_type": "user",
                }
            )

            return TokenResponse(
                access_token=token,
                token_type="bearer",
                user=UserOut(
                    id=user.id,
                    name=user.full_name,
                    email=user.email,
                    role=user.role,
                    status="active" if user.is_active else "inactive",
                ),
            )

        restaurant = await AuthRepository.get_restaurant_by_email(session, payload.email)
        if restaurant:
            if not verify_password(payload.password, restaurant.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            if restaurant.status != "approved":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Restaurant is not approved yet",
                )

            token = create_access_token(
                data={
                    "sub": str(restaurant.id),
                    "email": restaurant.owner_email,
                    "role": "restaurant",
                    "entity_type": "restaurant",
                }
            )

            return TokenResponse(
                access_token=token,
                token_type="bearer",
                user=UserOut(
                    id=restaurant.id,
                    name=restaurant.restaurant_name,
                    email=restaurant.owner_email,
                    role="restaurant",
                    status=restaurant.status,
                ),
            )

        delivery_agent = await AuthRepository.get_delivery_agent_by_email(
            session, payload.email
        )
        if delivery_agent:
            if not verify_password(payload.password, delivery_agent.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            if delivery_agent.status != "approved":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Delivery agent is not approved yet",
                )

            token = create_access_token(
                data={
                    "sub": str(delivery_agent.id),
                    "email": delivery_agent.email,
                    "role": "delivery_agent",
                    "entity_type": "delivery_agent",
                }
            )

            return TokenResponse(
                access_token=token,
                token_type="bearer",
                user=UserOut(
                    id=delivery_agent.id,
                    name=delivery_agent.full_name,
                    email=delivery_agent.email,
                    role="delivery_agent",
                    status=delivery_agent.status,
                ),
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    @staticmethod
    async def forgot_password(session: AsyncSession, payload: ForgotPasswordRequest):
        account = None
        entity_type = None

        user = await AuthRepository.get_user_by_email(session, payload.email)
        if user:
            account = user
            entity_type = "user"
        else:
            restaurant = await AuthRepository.get_restaurant_by_email(session, payload.email)
            if restaurant:
                account = restaurant
                entity_type = "restaurant"
            else:
                delivery_agent = await AuthRepository.get_delivery_agent_by_email(
                    session, payload.email
                )
                if delivery_agent:
                    account = delivery_agent
                    entity_type = "delivery_agent"

        if not account:
            return ForgotPasswordResponse(
                message="If the email exists, a reset token has been generated."
            )

        reset_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(reset_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

        await AuthRepository.create_reset_token(
            session=session,
            entity_type=entity_type,
            entity_id=account.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        return ForgotPasswordResponse(
            message="Password reset token generated successfully.",
            reset_token=reset_token,
        )

    @staticmethod
    async def reset_password(session: AsyncSession, payload: ResetPasswordRequest):
        token_hash = hashlib.sha256(payload.token.encode()).hexdigest()
        reset_token = await AuthRepository.get_reset_token_by_hash(session, token_hash)

        if (
            not reset_token
            or reset_token.is_used
            or reset_token.expires_at < datetime.now(timezone.utc)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        new_hashed_password = hash_password(payload.new_password)

        if reset_token.entity_type == "user":
            user = await AuthRepository.get_user_by_id(session, reset_token.entity_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            await AuthRepository.update_user_password(session, user, new_hashed_password)

        elif reset_token.entity_type == "restaurant":
            restaurant = await AuthRepository.get_restaurant_by_id(
                session, reset_token.entity_id
            )
            if not restaurant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Restaurant not found",
                )
            await AuthRepository.update_restaurant_password(
                session, restaurant, new_hashed_password
            )

        elif reset_token.entity_type == "delivery_agent":
            delivery_agent = await AuthRepository.get_delivery_agent_by_id(
                session, reset_token.entity_id
            )
            if not delivery_agent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Delivery agent not found",
                )
            await AuthRepository.update_delivery_agent_password(
                session, delivery_agent, new_hashed_password
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token type",
            )

        await AuthRepository.mark_reset_token_used(session, reset_token)
        return {"message": "Password reset successfully"}

    @staticmethod
    async def logout(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            exp = payload.get("exp")
            if exp is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token",
                )

            ttl = int(exp - datetime.now(timezone.utc).timestamp())
            if ttl < 0:
                ttl = 0

            token_key = f"blacklist:{token_fingerprint(token)}"
            await redis_client.setex(token_key, ttl, "1")

            return MessageResponse(message="Logged out successfully")

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token",
            )