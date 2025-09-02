from lib.lib_import import BaseModel, Optional, datetime
from models.cmh.cmh_allergy_model import AllergySeverityEnum, AllergyStatusEnum

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