from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, status, get_db,
)
from models.cmh.vital_snapshot_model import VitalSnapshotModel
from schema.cmh.vital_snapshot_schema import VitalCreateSchema, VitalResponseSchema

router = APIRouter(prefix="/vitals", tags=["Vitals"])

# create
@router.post("/", response_model=VitalResponseSchema)
def create_vital(vital: VitalCreateSchema, db: Session = Depends(get_db)):
    # exclude bmi if sent mistakenly
    vital_model = vital.model_dump(exclude = {"bmi"}, exclude_unset = True)

    new_vital = VitalSnapshotModel(**vital_model)
    db.add(new_vital)
    db.commit()
    db.refresh(new_vital)
    return new_vital

# get all
@router.get("/", response_model=List[VitalResponseSchema])
def get_vitals(db: Session = Depends(get_db)):
    return db.query(VitalSnapshotModel).filter(VitalSnapshotModel.is_active == True).all()

# get by id
@router.get("/{vital_id}", response_model=VitalResponseSchema)
def get_vital(vital_id: int, db: Session = Depends(get_db)):
    vital = db.query(VitalSnapshotModel).filter(
        VitalSnapshotModel.vital_id == vital_id,
        VitalSnapshotModel.is_active == True
    ).first()
    if not vital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = "Vital record not found"
        )
    return vital

# list by patient
@router.get("/patient/{patient_id}", response_model = List[VitalResponseSchema])
def get_vitals_for_patient(patient_id: int, db: Session = Depends(get_db)):
    return db.query(VitalSnapshotModel).filter(
        VitalSnapshotModel.patient_id == patient_id,
        VitalSnapshotModel.is_active == True
    ).order_by(VitalSnapshotModel.recorded_at.desc()).all()

# Update
@router.put("/{vital_id}", response_model=VitalResponseSchema)
def update_vital(vital_id: int, vital_data: VitalCreateSchema, db: Session = Depends(get_db)):
    vital = db.query(VitalSnapshotModel).filter(
        VitalSnapshotModel.vital_id == vital_id,
        VitalSnapshotModel.is_active == True
    ).first()

    if not vital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = "Vital record not found"
        )
    
    # exclude bmi if sent mistakenly
    update_data = vital_data.model_dump(exclude = {"bmi"}, exclude_unset = True)

    for key, value in update_data.items():
        setattr(vital, key, value)

    db.commit()
    db.refresh(vital)

    return vital

# Soft Delete
@router.delete("/{vital_id}")
def delete_vital(vital_id: int, db: Session = Depends(get_db)):
    vital = db.query(VitalSnapshotModel).filter(
        VitalSnapshotModel.vital_id == vital_id,
        VitalSnapshotModel.is_active == True
    ).first()
    if not vital:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Vital record not found"
        )

    vital.is_active = False
    db.commit()
    return {
        "message": "Vital record deleted successfully"
    }
