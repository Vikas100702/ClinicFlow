from lib.lib_import import Enum, BaseModel, Optional, datetime
from models.cmh.medical_condition_model import ConditionStatusEnum

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