from lib.lib_import import BaseModel, Optional, datetime
from models.lab_order_model import LabOrderStatusEnum

class LaborderCreateSchema(BaseModel):
    appointment_id: int
    test_name: str
    notes: Optional[str] = None

class LabOrderResponseSchema(BaseModel):
    id: int
    appointment_id: int
    test_name: str
    notes: Optional[str]
    status: LabOrderStatusEnum
    result_file_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
