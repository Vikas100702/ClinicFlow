from lib.lib_import import BaseModel, Optional, datetime

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