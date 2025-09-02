from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, status, get_db
)
from models.cmh.medication_model import MedicationStatementModel
from schema.cmh.medication_schema import MedicationCreateSchema, MedicationResponseSchema

router = APIRouter(prefix="/medications", tags=["Medications"])

# create medication
@router.post("/", response_model=MedicationResponseSchema)
def create_medication(med: MedicationCreateSchema, db: Session = Depends(get_db)):
    new_medication = MedicationStatementModel(**med.dict())
    db.add(new_medication)
    db.commit()
    db.refresh(new_medication)
    return new_medication

# get all medications
@router.get("/", response_model=List[MedicationResponseSchema])
def get_all_medications(db: Session = Depends(get_db)):
    return db.query(MedicationStatementModel).all()

# get by ID
@router.get("/{medication_id}", response_model=MedicationResponseSchema)
def get_medication(medication_id: int, db: Session = Depends(get_db)):
    medication = db.query(MedicationStatementModel).filter(
        MedicationStatementModel.medication_id == medication_id
    ).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication

# get by patient
@router.get("/patient/{patient_id}", response_model=List[MedicationResponseSchema])
def get_medications_by_patient(patient_id: int, db: Session = Depends(get_db)):
    medication = db.query(MedicationStatementModel).filter(
        MedicationStatementModel.patient_id == patient_id
    ).all()
    if not medication:
        raise HTTPException(status_code=404, detail="No medications found for this patient")
    return medication

# update medication
@router.put("/{medication_id}", response_model=MedicationResponseSchema)
def update_medication(
    medication_id: int,
    med_data: MedicationCreateSchema,
    db: Session = Depends(get_db)
):
    medication = db.query(MedicationStatementModel).filter(
        MedicationStatementModel.medication_id == medication_id
    ).first()
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Medication not found"
        )

    for key, value in med_data.dict(exclude_unset=True).items():
        setattr(medication, key, value)

    db.commit()
    db.refresh(medication)
    return medication

# deactivate medication
@router.patch("/{medication_id}/deactivate", response_model=MedicationResponseSchema)
def deactivate_medication(medication_id: int, db: Session = Depends(get_db)):
    medication = db.query(MedicationStatementModel).filter(
        MedicationStatementModel.medication_id == medication_id
    ).first()

    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Medication not found"
        )
    
    medication.is_active = False
    db.commit()
    db.refresh(medication)
    return medication

#soft delete
@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    medication = db.query(MedicationStatementModel).filter(
        MedicationStatementModel.medication_id == medication_id,
        MedicationStatementModel.is_active == True
    ).first()

    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")

    medication.is_active = False
    db.commit()
    return {"detail": "Medication deleted successfully"}