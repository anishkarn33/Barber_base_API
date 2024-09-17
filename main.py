from sqlite3 import IntegrityError
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Salon, User, Appointment, Service
from schemas import AppointmentResponse, SalonResponse, UserCreate, AppointmentCreate, ServiceCreate, UserResponse, ServiceResponse
from auth import authenticate_user, create_access_token, get_current_user, verify_password, hash_password
from utils import get_password_hash
from datetime import timedelta
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BarberBook API",
    description="API for barbers booking appointments",
    version="1.0.0")

models.Base.metadata.create_all(bind=engine)

appointment_router = APIRouter(prefix="/appointments", tags=["appointments"])
authentication_router = APIRouter(prefix="/auth", tags=["auth"])
user_management_router = APIRouter(prefix="/users", tags=["users management"])
service_router = APIRouter(prefix="/services", tags=["services"])
salon_router = APIRouter(prefix="/salons", tags=["salons"])

# Register user
@app.post("/register/", response_model=schemas.UserResponse,tags=["users management"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    
    # Create and add the new user
    hashed_password = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_barber=user.is_barber
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occurred while registering user.")
    
    return db_user

# Login and get token
@app.post("/token",tags=["auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# Book appointment
@app.post("/appointments", response_model=AppointmentResponse, tags=["appointments"])
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != appointment.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to book this appointment")

    existing_appointment = db.query(Appointment).filter(
        Appointment.barber_id == appointment.barber_id,
        Appointment.time == appointment.time
    ).first()
    
    if existing_appointment:
        raise HTTPException(status_code=400, detail="Barber is already booked at this time")
    
    db_appointment = Appointment(
        user_id=appointment.user_id,
        barber_id=appointment.barber_id,
        time=appointment.time  
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment



@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse, tags=["appointments"])
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@app.get("/appointments", response_model=List[AppointmentResponse], tags=["appointments"])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

# Add services
@app.post("/services/", response_model=ServiceResponse, tags=["services"])
def add_service(service: ServiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_barber:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only barbers can add services.")
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

# List services
@app.get("/services/", response_model=list[ServiceResponse], tags=["services"])
def list_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services



# Register salon
@app.post("/register-salon/", response_model=schemas.SalonResponse, tags=["salons"])
def register_salon(salon: schemas.SalonCreate, db: Session = Depends(get_db)):
    # Ensure the salon name does not already exist
    existing_salon = db.query(models.Salon).filter(models.Salon.name == salon.name).first()
    if existing_salon:
        raise HTTPException(status_code=400, detail="Salon name already registered.")

    owner = db.query(models.User).filter(models.User.id == salon.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found.")

    # Create a new salon
    db_salon = models.Salon(
        name=salon.name,
        address=salon.address,
        owner=owner  
    )
    db.add(db_salon)
    db.commit()
    db.refresh(db_salon)

    return db_salon


    return db_salon
# List salons
@app.get("/salons", response_model=List[SalonResponse], tags=["salons"])
async def list_salons(db: Session = Depends(get_db)):
    salons = db.query(Salon).all()
    return [
        {
            "id": salon.id,
            "name": salon.name,
            "address": salon.address,
            "owner": salon.owner.name,  
            "description": salon.description  or ""
        }
        for salon in salons
    ]
# Get salon details
@app.get("/salons/{salon_id}", response_model=schemas.SalonResponse, tags=["salons"])
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    salon = db.query(models.Salon).filter(models.Salon.id == salon_id).first()
    if salon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Salon not found")
    return salon

# Update salon
@app.put("/salons/{salon_id}", response_model=schemas.SalonResponse, tags=["salons"])
def update_salon(salon_id: int, salon_update: schemas.SalonUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    salon = db.query(models.Salon).filter(models.Salon.id == salon_id).first()
    if salon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Salon not found")
    
    if salon.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this salon")
    
    for key, value in salon_update.dict().items():
        setattr(salon, key, value)
    
    db.commit()
    db.refresh(salon)
    return salon

# Delete salon
@app.delete("/salons/{salon_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["salons"])
def delete_salon(salon_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    salon = db.query(models.Salon).filter(models.Salon.id == salon_id).first()
    if salon is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Salon not found")
    
    if salon.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this salon")
    
    db.delete(salon)
    db.commit()