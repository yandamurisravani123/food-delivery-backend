from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from uuid import UUID


class RegisterSuperAdmin(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)
    phone: Optional[str] = Field(default=None, max_length=20)

    role:Literal["super_admin","user"]
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v):
        if v.strip().lower() == "string":
            raise ValueError("Please enter valid full name")
        return v
 
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v.lower() == "user@example.com":
            raise ValueError("Please enter valid email address")
        return v
 
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v.strip().lower() == "string":
            raise ValueError("Please enter valid phone number")
        return v
 
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v.strip().lower() == "string":
            raise ValueError("Please enter valid password")
 
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
 
        return v


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class ResendOtpRequest(BaseModel):
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    role: str
    status: Optional[str] = None
    is_active: Optional[bool] = None

class RegisterResponse(BaseModel):
    message: str
    user: UserOut


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    message: str
    reset_token: Optional[str] = None


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=20)
    new_password: str = Field(..., min_length=8, max_length=128)


class MessageResponse(BaseModel):
    message: str