from lib.lib_import import (
    Base, Column, Integer, String, Enum, DateTime, 
    datetime, timezone, enum
)

class GenderEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHERS = "OTHERS"

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"

class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(10), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)