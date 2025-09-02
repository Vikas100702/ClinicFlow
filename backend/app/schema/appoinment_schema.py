from lib.lib_import import Enum, BaseModel, datetime, Optional
from models.appointment_model import AppointmentStatus

class AppointmentSchema(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    disease: Optional[str] = None
    status: Optional[AppointmentStatus] = AppointmentStatus.booked

class AppointmentCreateSchema(AppointmentSchema):
    pass

class AppointmentResponseSchema(AppointmentSchema):
    appointment_id: int
    created_at: datetime
    updated_at: datetime

    class config:
        from_attributes = True