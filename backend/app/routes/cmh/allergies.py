from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, status, get_db,
)
from models.cmh.cmh_allergy_model import MedicalAllergyModel
from schema.cmh.allergy_schema import AllergyCreateSchema, AllergyResponseSchema

router = APIRouter(prefix = "/allergies", tags = ["Allergies"])

# Patient creates allergy
@router.post("/", response_model = AllergyResponseSchema)
def create_allergy_for_patient(allergy: AllergyCreateSchema, db: Session = Depends(get_db)):
    new_allergy = MedicalAllergyModel(**allergy.model_dump())
    db.add(new_allergy)
    db.commit()
    db.refresh(new_allergy)

    return new_allergy

# Doctor creates allergy
@router.post("/doctor", response_model = AllergyResponseSchema)
def create_allergy_by_doctor(allergy: AllergyCreateSchema, db: Session = Depends(get_db)):
    new_allergy = MedicalAllergyModel(**allergy.model_dump())
    db.add(new_allergy)
    db.commit()
    db.refresh(new_allergy)

    return new_allergy

# Patient gets own allergies
@router.get("/{patient_id}", response_model = List[AllergyResponseSchema])
def get_patient_allergy(patient_id: int, db: Session = Depends(get_db)):
    allergies = db.query(MedicalAllergyModel).filter(MedicalAllergyModel.patient_id == patient_id).all()
    if not allergies:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No allergies found for this patient"
        )
    
    return allergies

# Doctor gets patient allergies
@router.get("/doctor/{patient_id}", response_model = List[AllergyResponseSchema])
def doctor_get_patient_allergy(patient_id: int, db: Session = Depends(get_db)):
    allergies = db.query(MedicalAllergyModel).filter(MedicalAllergyModel.patient_id == patient_id).all()
    if not allergies:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No allergies found for this patient"
        )
    
    return allergies

# Update allergy (Patient/Doctor)
@router.put("/{allergy_id}", response_model = AllergyResponseSchema)
def update_allergy(allergy_id: int, allergy_update: AllergyCreateSchema, db: Session = Depends(get_db)):
    allergy = db.query(MedicalAllergyModel).filter(MedicalAllergyModel.allergy_id == allergy_id).first()

    if not allergy:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Allergy Not Found"
        )
    
    for key, value in allergy_update.model_dump().items():
        setattr(allergy, key, value)

    db.commit()
    db.refresh(allergy)

    return allergy

# Delete allergy (soft delete → set is_active=False)
@router.delete("/{allergy_id}")
def delete_allergy(allergy_id: int, db: Session = Depends(get_db)):
    allergy = db.query(MedicalAllergyModel).filter(MedicalAllergyModel.allergy_id == allergy_id).first()

    if not allergy:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Allergy Not Found"
        )
    
    allergy.is_active = False # soft delete

    db.commit()

    return {
        "message": f"Allergy {allergy_id} marked as inactive"
    }