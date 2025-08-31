from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TimelineEntrySchema(BaseModel):
    date: datetime
    type: str
    summary: str
    reference_id: int
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None

    class Config:
        from_attributes = True

class TimelineResponseSchema(BaseModel):
    patient_id: int
    timeline: List[TimelineEntrySchema]