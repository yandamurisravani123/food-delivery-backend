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

        await redis_client.setex(f"otp:{payload.email.lower()}", 600, otp_hash)
        await send_otp_email(payload.email, otp)

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

        stored_hash = await redis_client.get(f"otp:{payload.email.lower()}")

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

        await redis_client.delete(f"otp:{payload.email.lower()}")

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

        await redis_client.setex(
            f"otp:{payload.email.lower()}",
            600,
            otp_hash
        )

        try:
            await send_otp_email(payload.email, otp)
        except Exception as e:
            print("EMAIL ERROR:", str(e))

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

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    @staticmethod
    async def forgot_password(session: AsyncSession, payload: ForgotPasswordRequest):
        user = await AuthRepository.get_user_by_email(session, payload.email)

        if not user:
            return ForgotPasswordResponse(
                message="If the email exists, a reset token has been generated."
            )

        reset_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(reset_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

        await AuthRepository.create_reset_token(
            session=session,
            entity_type="user",
            entity_id=user.id,
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

        user = await AuthRepository.get_user_by_id(session, reset_token.entity_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await AuthRepository.update_user_password(session, user, new_hashed_password)
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
            ttl = int(exp - datetime.now(timezone.utc).timestamp())

            if ttl < 0:
                ttl = 0

            await redis_client.setex(
                f"blacklist:{token_fingerprint(token)}",
                ttl,
                "1"
            )

            return MessageResponse(message="Logged out successfully")

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token",
            )