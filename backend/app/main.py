from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from database.database import get_db, Base
from models import UserModel, DoctorModel, PatientModel
from schemas import UserLoginSchema, TokenResponseSchema
from core.security import hash_password, verify_password
from core.jwt import create_access_token
from core.dependency import decode_access_token, get_current_user
from core.roles import role_checker

from routes import (
    appointments, doctor_availability, dashboard, forgot_password,
    prescriptions, lab_orders
)

from routes.cmh import (
    allergies, conditions, medication, immunization, 
    procedures, encounter_notes, medical_doc, vitals,
    summary
)

from schemas import (
    UserCreateSchema, UserResponseSchema,
    DoctorCreateSchema, DoctorResponseSchema,
    PatientCreateSchema, PatientResponseSchema
)

app = FastAPI(title="ClinicFlow APP", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)  

app.include_router(appointments.router)
app.include_router(doctor_availability.router)
app.include_router(dashboard.router)
app.include_router(forgot_password.router)
app.include_router(prescriptions.router)
app.include_router(lab_orders.router)
app.include_router(allergies.router)
app.include_router(conditions.router)
app.include_router(medication.router)
app.include_router(immunization.router)
app.include_router(procedures.router)
app.include_router(encounter_notes.router)
app.include_router(medical_doc.router)
app.include_router(vitals.router)
app.include_router(summary.router)

# User Registration
@app.post("/register/user", response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    new_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        email=user.email,
        phone_number=user.phone_number,
        role=user.role,
        password_hash=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# Doctor Registration
@app.post("/register/doctor", response_model=DoctorResponseSchema)
def register_doctor(doctor: DoctorCreateSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.user_id == doctor.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "DOCTOR":
        raise HTTPException(status_code=400, detail="User is not assigned as Doctor")

    new_doctor = DoctorModel(**doctor.model_dump())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor



# Patient Registration
@app.post("/register/patient", response_model=PatientResponseSchema)
def register_patient(patient: PatientCreateSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.user_id == patient.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "PATIENT":
        raise HTTPException(status_code=400, detail="User is not assigned as Patient")

    new_patient = PatientModel(**patient.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

# get all user data
@app.get("/users/", response_model=List[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

# Login API
@app.post("/login", response_model = TokenResponseSchema)
def login(login_data: UserLoginSchema, db: Session = Depends(get_db)):
    # Search User in DB
    user = db.query(UserModel).filter(UserModel.email == login_data.email).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password",
        )

    # Verify Password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid password",
        )

    # Create JWT token
    access_token = create_access_token(
        data = {
            "sub": str(user.user_id),
            "role": user.role
        }
    )

    return TokenResponseSchema(access_token = access_token)

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user['sub']}! Your role is {current_user['role']}."
    }
