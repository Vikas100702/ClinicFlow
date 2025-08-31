from pydantic import BaseModel, EmailStr, StringConstraints, field_validator
from typing import Annotated, List
from datetime import datetime, time
from typing import Optional, List
from enum import Enum
from models.user_role_model import GenderEnum, RoleEnum
from models.lab_order_model import LabOrderStatusEnum
from models.cmh.cmh_allergy_model import AllergySeverityEnum, AllergyStatusEnum
from models.cmh.procedure_model import ProcedureStatusEnum
import re

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

# Appointment Schema
class AppoinmentStatus(str, Enum):
    booked = "BOOKED"
    confirmed = "CONFIRMED"
    completed = "COMPLETED"
    cancelled = "CANCELLED"

class AppointmentSchema(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    disease: Optional[str] = None
    status: Optional[AppoinmentStatus] = AppoinmentStatus.booked

class AppointmentCreateSchema(AppointmentSchema):
    pass

class AppointmentResponseSchema(AppointmentSchema):
    appointment_id: int
    created_at: datetime
    updated_at: datetime

    class config:
        from_attributes = True

# Doctor Availability Schema
class DoctorAvailabilitySchema(BaseModel):
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time
    is_active: Optional[bool] = True

class DoctorAvailabilityCreateSchema(DoctorAvailabilitySchema):
    pass
class DoctorAvailabilityResponseSchema(DoctorAvailabilitySchema):
    availability_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Prescription Schema
class PrescriptionBase(BaseModel):
    appoinment_id: int
    doctor_id: int
    patient_id: int
    medicines: str
    note: Optional[str] = None

class PrescriptionCreateSchema(PrescriptionBase):
    pass

class PrescriptionResponseSchema(PrescriptionBase):
    prescription_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# lab order schema
class LaborderCreateSchema(BaseModel):
    appointment_id: int
    test_name: str
    notes: Optional[str] = None

class LabOrderResponseSchema(BaseModel):
    id: int
    appointment_id: int
    test_name: str
    notes: Optional[str]
    status: LabOrderStatusEnum
    result_file_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# cmh allergy schema
class AllergyBaseSchema(BaseModel):
    substance: str
    reaction: Optional[str] = None
    severity: Optional[AllergySeverityEnum] = None
    status: Optional[AllergyStatusEnum] = AllergyStatusEnum.active

class AllergyCreateSchema(AllergyBaseSchema):
    patient_id: int
    doctor_id: int

class AllergyResponseSchema(AllergyBaseSchema):
    allergy_id: int
    patient_id: int
    doctor_id: int
    recorded_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Medical Condition Schema
class ConditionStatusEnum(str, Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"
    resolved = "RESOLVED"

class ConditionCreateSchema(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    condition_name: str
    description: Optional[str] = None
    status: ConditionStatusEnum = ConditionStatusEnum.active

class ConditionUpdateSchema(BaseModel):
    doctor_id: Optional[int] = None
    condition_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ConditionStatusEnum] = None

class ConditionResponseSchema(ConditionCreateSchema):
    condition_id: int
    diagnosed_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Medication Statement Schema
class MedicationCreateSchema(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    medication_name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    instructions: Optional[str] = None

class MedicationResponseSchema(MedicationCreateSchema):
    medication_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Immunization Schema
class ImmunizationStatusEnum(str, Enum):
    completed = "COMPLETED"
    pending = "PENDING"
    cancelled = "CANCELLED"

# create immunization
class ImmunizationCreateSchema(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    vaccine_name: str
    dose_number: Optional[int] = None
    status: ImmunizationStatusEnum = ImmunizationStatusEnum.completed
    notes: Optional[str] = None

# update immunization
class ImmunizationUpdateSchema(BaseModel):
    vaccine_name: Optional[str] = None
    dose_number: Optional[int] = None
    status: Optional[ImmunizationStatusEnum] = None
    notes: Optional[str] = None

# response schema
class ImmunizationResponseSchema(ImmunizationCreateSchema):
    immunization_id: int
    administered_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Procedure Schema
class ProcedureCreateSchema(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    procedure_name: str
    description: Optional[str] = None
    status: ProcedureStatusEnum = ProcedureStatusEnum.scheduled
    performed_at: Optional[datetime] = None

class ProcedureUpdateSchema(BaseModel):
    procedure_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProcedureStatusEnum] = None
    performed_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class ProcedureResponseSchema(ProcedureCreateSchema):
    procedure_id: int
    recorded_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# encounter notes schema
class EncounterNoteCreateSchema(BaseModel):
    patient_id: int
    doctor_id: int
    title: str
    content: str

class EncounterNoteUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None

class EncounterNoteResponseSchema(EncounterNoteCreateSchema):
    note_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True

# medical doc schema
class MedicalDocumentCreateSchema(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    title: str

class MedicalDocumentResponseSchema(MedicalDocumentCreateSchema):
    document_id: int
    file_path: str
    file_type: str
    uploaded_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# vital snapshot schema
class VitalCreateSchema(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature: Optional[float] = None
    oxygen_saturation: Optional[float] = None

class VitalResponseSchema(VitalCreateSchema):
    vital_id: int
    bmi: Optional[float] = None
    recorded_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
