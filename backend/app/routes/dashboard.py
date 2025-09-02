from lib.lib_import import (
    APIRouter, HTTPException, Depends, Session, func, get_current_user, get_db
)
from models.user_role_model import UserModel
from models.patient_model import PatientModel
from models.doctor_model import DoctorModel
from models.appointment_model import AppointmentModel

router = APIRouter(prefix = "/dashboard", tags = ["Dashboard"])

# Patient Dashboard
@router.get("/patient")
def patient_dashboard(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    # check role
    patient = db.query(PatientModel).filter_by(user_id=current_user.user_id).first()
    if not patient:
        raise HTTPException(status_code=403, detail="Not a patient")

    # 1. Doctors list
    doctors = db.query(DoctorModel, UserModel).join(UserModel, DoctorModel.user_id == UserModel.user_id).all()
    doctor_list = [{
        "doc_id": d.DoctorModel.doc_id,
        "name": f"{d.UserModel.first_name} {d.UserModel.last_name}",
        "specialization": d.DoctorModel.specialization,
        "qualification": d.DoctorModel.qualification,
        "experience": d.DoctorModel.experience,
        "bio": d.DoctorModel.bio,
        "available_days": d.DoctorModel.available_days,
    } for d in doctors]

    # 2. My upcoming appointments
    appts = db.query(AppointmentModel, DoctorModel, UserModel)\
        .join(DoctorModel, AppointmentModel.doctor_id == DoctorModel.doc_id)\
        .join(UserModel, DoctorModel.user_id == UserModel.user_id)\
        .filter(AppointmentModel.patient_id == patient.patient_id,
                AppointmentModel.start_time >= func.now())\
        .order_by(AppointmentModel.start_time).all()

    my_appts = [{
        "appointment_id": a.AppointmentModel.appointment_id,
        "start_time": a.AppointmentModel.start_time,
        "end_time": a.AppointmentModel.end_time,
        "status": a.AppointmentModel.status,
        "doctor": f"{a.UserModel.first_name} {a.UserModel.last_name}",
        "specialization": a.DoctorModel.specialization,
    } for a in appts]

    return {"doctors": doctor_list, "my_appointments": my_appts}

# Doctor Dashboard
@router.get("/doctor")
def doctor_dashboard(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    # check role
    doctor = db.query(DoctorModel).filter_by(user_id=current_user.user_id).first()
    if not doctor:
        raise HTTPException(status_code=403, detail="Not a doctor")

    # 1. Today's appointments
    today_appts = db.query(AppointmentModel, PatientModel, UserModel)\
        .join(PatientModel, AppointmentModel.patient_id == PatientModel.patient_id)\
        .join(UserModel, PatientModel.user_id == UserModel.user_id)\
        .filter(AppointmentModel.doctor_id == doctor.doc_id,
                func.date(AppointmentModel.start_time) == func.current_date())\
        .order_by(AppointmentModel.start_time).all()

    appts_today = [{
        "appointment_id": a.AppointmentModel.appointment_id,
        "time": a.AppointmentModel.start_time,
        "status": a.AppointmentModel.status,
        "patient": f"{a.UserModel.first_name} {a.UserModel.last_name}",
    } for a in today_appts]

    # 2. My patients list
    patients = db.query(UserModel).join(PatientModel, UserModel.user_id == PatientModel.user_id)\
        .join(AppointmentModel, AppointmentModel.patient_id == PatientModel.patient_id)\
        .filter(AppointmentModel.doctor_id == doctor.doc_id).distinct().all()

    patient_list = [{
        "id": p.user_id,
        "name": f"{p.first_name} {p.last_name}",
        "email": p.email,
        "phone": p.phone_number,
    } for p in patients]

    # 3. Stats
    stats = db.query(AppointmentModel.status, func.count(AppointmentModel.appointment_id))\
        .filter(AppointmentModel.doctor_id == doctor.doc_id)\
        .group_by(AppointmentModel.status).all()
    stats_dict = {s[0]: s[1] for s in stats}

    return {"today_appointments": appts_today, "patients": patient_list, "stats": stats_dict}
