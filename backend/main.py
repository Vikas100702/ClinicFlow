from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.database.database import get_db, Base
from app.models import UserModel, DoctorModel, PatientModel
from app.schemas import UserLoginSchema, TokenResponseSchema
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.dependency import decode_access_token, get_current_user
from app.core.roles import role_checker

from app.schemas import (
    UserCreateSchema, UserResponseSchema,
    DoctorCreateSchema, DoctorResponseSchema,
    PatientCreateSchema, PatientResponseSchema
)

app = FastAPI(title="ClinicFlow APP", version="1.0.0")

# User Registration
@app.post("/register/user", response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)

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
            detail = "Invalid email or password",
        )

    # Create JWT token
    access_token = create_access_token(
        data = {
            "sub": user.email,
            "role": user.role
        }
    )

    return TokenResponseSchema(access_token = access_token)

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user['sub']}! Your role is {current_user['role']}."
    }

# for doctors only
@app.get("/doctor/dashboard")
def doctor_dashboard(current_user: dict = Depends(role_checker("doctor"))):
    return {
        "message": f"Welcome Dr. {current_user['sub']}"
    }

# for patient only
@app.get("/patient/dashboard")
def patient_dashboard(current_user: dict = Depends(role_checker("patient"))):
    return {"msg": f"Welcome Patient {current_user['sub']}"}
