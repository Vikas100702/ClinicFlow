from lib.lib_import import BaseModel, Optional, datetime
from models.cmh.procedure_model import ProcedureStatusEnum

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