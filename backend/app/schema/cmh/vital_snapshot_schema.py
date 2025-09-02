from lib.lib_import import BaseModel, Optional, datetime

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
