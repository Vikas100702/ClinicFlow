from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List

from database.database import get_db
from models.appointment_model import AppointmentModel
from schemas import AppointmentCreateSchema, AppointmentResponseSchema

router = APIRouter(prefix = "/appointments", tags = ["Appointments"])

@router.post("/", response_model = AppointmentResponseSchema)
def create_appointment(payload: AppointmentCreateSchema, db: Session = Depends(get_db)):
    # appointment overlap check
    overlap = db.query(AppointmentModel).filter(
        AppointmentModel.doctor_id == payload.doctor_id,
        AppointmentModel.start_time < payload.end_time,
        AppointmentModel.end_time > payload.start_time
    ).first()

    if overlap:
        raise HTTPException(status_code = 400, detail = "Doctor already has appointment in this slot.")
    
    appointment = AppointmentModel(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

@router.get("/{appointment_id}", response_model = AppointmentResponseSchema)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(AppointmentModel).get(appointment_id)

    if not appointment:
        raise HTTPException(status_code = 404, detail = "Appointment Not Found")
    return appointment

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(AppointmentModel).get(appointment_id)

    if not appointment:
        raise HTTPException(status_code = 404, detail = "Appointmnet Not Found")
    
    db.delete(appointment)
    db.commit()
    
    return {
        "message": "Appointment deleted successfully"
    }
    
