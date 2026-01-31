from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status: bool
    detail: Optional[T] = None
    message: str

class UserBase(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    country: str = Field(...)
    state: str = Field(...)
    city: str = Field(...)
    role_id: int = Field(...,gt=0)

class UserCreate(UserBase):
    password: str = Field(...)
    model_config = ConfigDict(from_attributes=True) 

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True) 


class RoleBase(BaseModel):
    role_name: str = Field(...)   # patient, caregiver, physician, admin

class RoleResponse(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)     

class Login(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None