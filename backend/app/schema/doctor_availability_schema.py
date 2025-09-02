from lib.lib_import import BaseModel, time, datetime, Optional

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