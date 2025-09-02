from lib.lib_import import BaseModel, EmailStr, datetime, field_validator, re
from models.user_role_model import GenderEnum, RoleEnum
from schema.common_types import NameType, PhoneType

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