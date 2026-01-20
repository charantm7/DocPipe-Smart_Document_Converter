from typing import Optional
from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginSchema(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class SignupSchema(LoginSchema, BaseModel):

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
