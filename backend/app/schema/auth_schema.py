from lib.lib_import import BaseModel, EmailStr

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"