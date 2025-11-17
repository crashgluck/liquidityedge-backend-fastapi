from pydantic import BaseModel, EmailStr, Field

from typing import Optional


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(..., max_length=72)
    role: str  # investor | fund_manager | admin

    # Nuevos atributos del diseño de la BD
    name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    mobile: Optional[str] = None
    business_type: Optional[str] = None
    terms_accepted: bool = False
    terms_accepted_date: Optional[str] = None  # o datetime según tu preferencia
    portal_used: Optional[str] = None
    total_investment: Optional[int] = 0

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Send2FARequest(BaseModel):
    email: EmailStr

class Verify2FARequest(BaseModel):
    email: EmailStr
    code: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
