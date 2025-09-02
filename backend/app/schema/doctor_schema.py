from lib.lib_import import BaseModel
from schema.user_schema import UserResponseSchema
from schema.common_types import Text100, Text1000

class DoctorCreateSchema(BaseModel):
    user_id: int
    specialization: Text100
    qualification: Text100
    experience: str | None = None
    bio: Text1000 | None = None
    available_days: Text100 | None = None

class DoctorResponseSchema(BaseModel):
    doc_id: int
    user_id: int
    specialization: str
    qualification: str
    experience: str | None = None
    bio: str | None = None
    available_days: str | None = None
    user: UserResponseSchema

    class Config:
        from_attributes = True