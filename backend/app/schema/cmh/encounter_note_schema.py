from lib.lib_import import BaseModel, Optional, datetime

class EncounterNoteCreateSchema(BaseModel):
    patient_id: int
    doctor_id: int
    title: str
    content: str

class EncounterNoteUpdateSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None

class EncounterNoteResponseSchema(EncounterNoteCreateSchema):
    note_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True