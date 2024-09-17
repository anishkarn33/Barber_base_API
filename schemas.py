from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_barber: bool

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_barber: bool

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    user_id: int
    barber_id: int
    time: datetime

class AppointmentResponse(BaseModel):
    id: int
    time: datetime
    user: UserResponse
    barber: UserResponse

    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    name: str
    description: str
    price: int

class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int

    class Config:
        from_attributes = True

class SalonBase(BaseModel):
    name: str
    address: str
    description: str

class SalonCreate(SalonBase):
    name: str
    address: str
    owner_id: int

class SalonUpdate(SalonBase):
    pass

class SalonResponse(SalonBase):
    id: int
    name: str
    address: str
    owner: str
    description: str 

    class Config:
        from_attributes = True