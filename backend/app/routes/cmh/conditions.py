from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, get_db, status    
)
from schema.cmh.medical_condition_schema import (
    ConditionCreateSchema, ConditionResponseSchema, ConditionStatusEnum, ConditionUpdateSchema
)
from models.cmh.medical_condition_model import MedicalConditionModel

router = APIRouter(prefix = "/conditions", tags = ["Medical Conditions"])

# create
@router.post("/", response_model = ConditionResponseSchema)
def create_condition(condition: ConditionCreateSchema, db: Session = Depends(get_db)):
    new_condition = MedicalConditionModel(**condition.model_dump())

    db.add(new_condition)
    db.commit()
    db.refresh(new_condition)

    return new_condition

#get all by patient
@router.get("/patient/{patient_id}", response_model = List[ConditionResponseSchema])
def get_conditions(patient_id: int, db: Session = Depends(get_db)):
    return db.query(MedicalConditionModel).filter(
        MedicalConditionModel.patient_id == patient_id,
        MedicalConditionModel.is_active == True
    ).all()

# update condition
@router.put("/{condition_id}", response_model=ConditionResponseSchema)
def update_condition(
    condition_id: int,
    condition_data: ConditionUpdateSchema,
    db: Session = Depends(get_db)
):
    condition = db.query(MedicalConditionModel).filter(
        MedicalConditionModel.condition_id == condition_id,
        MedicalConditionModel.is_active == True
    ).first()

    if not condition:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Medical Condition Not Found"
        )
    
    update_data = condition_data.model_dump(exclude_unset = True)

    for key, value in update_data.items():
        setattr(condition, key, value)

    db.commit()
    db.refresh(condition)

    return condition

# deactivate condition
@router.patch("/{condition_id}/deactivate", response_model=ConditionResponseSchema)
def deactivate_condition(
    condition_id: int,
    db: Session = Depends(get_db)
):
    condition = db.query(MedicalConditionModel).filter(
        MedicalConditionModel.condition_id == condition_id,
        MedicalConditionModel.is_active == True
    ).first()

    if not condition:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Medical Condition Not Found"
        )
    
    condition.is_active = False
    condition.status = ConditionStatusEnum.inactive

    db.commit()
    db.refresh(condition)

    return condition

# get all ACTIVE conditions
@router.get("/", response_model = List[ConditionResponseSchema])
def get_active_condition(db: Session = Depends(get_db)):
    conditions = db.query(MedicalConditionModel).filter(MedicalConditionModel.is_active == True).all()

    return conditions

# get ALL conditions (including inactive)
@router.get("/all", response_model=List[ConditionResponseSchema])
def get_all_conditions(db: Session = Depends(get_db)):
    conditions = db.query(MedicalConditionModel).all()

    return conditions

# get condition by ID
@router.get("/{condition_id}", response_model=ConditionResponseSchema)
def get_condition_by_id(condition_id: int, db: Session = Depends(get_db)):
    condition = db.query(MedicalConditionModel).filter(
        MedicalConditionModel.condition_id == condition_id
    ).first()

    if not condition:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Medical Condition Not Found"
        )

    return condition

# soft delete
@router.delete("/{condition_id}")
def delete_condition(condition_id: int, db: Session = Depends(get_db)):
    condition = db.query(MedicalConditionModel).filter(MedicalConditionModel.condition_id == condition_id).first()

    if not condition:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Medical Condition Not Found"
        )
    
    condition.is_active = False
    db.commit()

    return {
        "message": "Medical Condition Deleted Successfully"
    }
