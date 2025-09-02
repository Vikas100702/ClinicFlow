from lib.lib_import import BaseModel
from schema.user_schema import UserResponseSchema
from schema.common_types import AddressType

class PatientCreateSchema(BaseModel):
    user_id: int
    address: AddressType | None = None


class PatientResponseSchema(BaseModel):
    patient_id: int
    user_id: int
    address: str | None = None
    user: UserResponseSchema

    class Config:
        from_attributes = True