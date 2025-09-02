from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, get_db, hash_password,
)
from models.user_role_model import UserModel
from models.patient_model import PatientModel
from models.doctor_model import DoctorModel
from schema.user_schema import UserResponseSchema, UserCreateSchema
from schema.patient_schema import PatientCreateSchema, PatientResponseSchema
from schema.doctor_schema import DoctorCreateSchema, DoctorResponseSchema

router = APIRouter(prefix="/register", tags=["Registration"])

# User Registration
@router.post("/user", response_model=UserResponseSchema)
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
@router.post("/doctor", response_model=DoctorResponseSchema)
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
@router.post("/patient", response_model=PatientResponseSchema)
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


# Get all Users
@router.get("/users", response_model=List[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users
