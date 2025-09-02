from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, func, get_db,
)
from models.doctor_availability_model import DoctorAvailabilityModel
from schema.doctor_availability_schema import (
    DoctorAvailabilityCreateSchema, DoctorAvailabilityResponseSchema
)

router = APIRouter(prefix = "/availability", tags = ["Doctor Availability"])

@router.post("/", response_model = DoctorAvailabilityResponseSchema)
def create_doc_availability(payload: DoctorAvailabilityCreateSchema, db: Session = Depends(get_db)):
    availability = DoctorAvailabilityModel(**payload.model_dump())

    db.add(availability)
    db.commit()
    db.refresh(availability)

    return availability

@router.get("/", response_model = List[DoctorAvailabilityResponseSchema])
def list_availabilities(db: Session = Depends(get_db)):
    return db.query(DoctorAvailabilityModel).all()

@router.get("/{availability_id}", response_model=DoctorAvailabilityResponseSchema)
def get_availability(availability_id: int, db: Session = Depends(get_db)):
    avail = db.query(DoctorAvailabilityModel).get(availability_id)
    if not avail:
        raise HTTPException(status_code=404, detail="Availability not found")
    return avail


@router.delete("/{availability_id}")
def delete_availability(availability_id: int, db: Session = Depends(get_db)):
    avail = db.query(DoctorAvailabilityModel).get(availability_id)
    if not avail:
        raise HTTPException(status_code=404, detail="Availability not found")
    db.delete(avail)
    db.commit()
    return {"message": "Availability deleted"}