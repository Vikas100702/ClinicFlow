from lib.lib_import import BaseModel, Optional, datetime

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
