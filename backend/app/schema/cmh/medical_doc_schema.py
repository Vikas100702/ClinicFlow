from lib.lib_import import BaseModel, Optional, datetime

class MedicalDocumentCreateSchema(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    title: str

class MedicalDocumentResponseSchema(MedicalDocumentCreateSchema):
    document_id: int
    file_path: str
    file_type: str
    uploaded_at: datetime
    is_active: bool

    class Config:
        from_attributes = True