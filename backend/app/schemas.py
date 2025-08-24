from pydantic import BaseModel, EmailStr, StringConstraints, field_validator
from typing import Annotated, List
from datetime import datetime
import re
from app.models.user_role_model import GenderEnum, RoleEnum

# Reusable Types
NameType = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=50, pattern=r'^[A-Za-z ]+$')]
PhoneType = Annotated[str, StringConstraints(pattern=r'^[0-9]{10}$')]
AddressType = Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]
Text100 = Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)]
Text1000 = Annotated[str, StringConstraints(strip_whitespace=True, max_length=1000)]

# User Schemas
class UserCreateSchema(BaseModel):
    first_name: NameType
    last_name: NameType
    gender: GenderEnum
    email: EmailStr
    phone_number: PhoneType
    role: RoleEnum
    password: str

    @field_validator("password")
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*()~`]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserResponseSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    gender: GenderEnum
    email: EmailStr
    phone_number: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True

# Doctor Schemas
class DoctorCreateSchema(BaseModel):
    user_id: int
    specialization: Text100
    qualification: Text100
    experience: str | None = None
    bio: Text1000 | None = None
    available_days: Text100 | None = None


class DoctorResponseSchema(BaseModel):
    doc_id: int
    user_id: int
    specialization: str
    qualification: str
    experience: str | None = None
    bio: str | None = None
    available_days: str | None = None
    user: UserResponseSchema

    class Config:
        from_attributes = True

# Patient Schemas
class PatientCreateSchema(BaseModel):
    user_id: int
    address: AddressType | None = None


class PatientResponseSchema(BaseModel):
    patient_id: int
    user_id: int
    address: str | None = None
    user: UserResponseSchema

    class Config:
        from_attributes = True


# User Login Schema
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"



