from lib.lib_import import (
    APIRouter, HTTPException, Session, Depends, status, get_db, List
)
from models.prescription_model import PrescriptionModel
from schema.prescription_schema import PrescriptionCreateSchema, PrescriptionResponseSchema

router = APIRouter(prefix = "/prescriptions", tags = ["Prescriptions"])

# create prescriptions
@router.post("/", response_model = PrescriptionCreateSchema)
def create_prescription(prescription: PrescriptionCreateSchema, db: Session = Depends(get_db)):
    new_presc = PrescriptionModel(**prescription.model_dump())

    db.add(new_presc)
    db.commit()
    db.refresh(new_presc)

    return new_presc

# get prescription for a patient
@router.get("/patient/{patient_id}", response_model = List[PrescriptionResponseSchema])
def get_patient_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    presc = db.query(PrescriptionModel).filter(PrescriptionModel.patient_id == patient_id).all()

    return presc

# get prescription by id
@router.get("/{prescription_id}", response_model = PrescriptionResponseSchema)
def get_prescription(presc_id: int, db: Session = Depends(get_db)):
    presc = db.query(PrescriptionModel).filter(PrescriptionModel.presc_id == presc_id).first()

    if not presc:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Prescription not found"
        )
    
    return presc