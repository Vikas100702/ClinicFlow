from lib.lib_import import Enum, BaseModel, Optional, datetime
from models.cmh.immunization_model import ImmunizationStatusEnum

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