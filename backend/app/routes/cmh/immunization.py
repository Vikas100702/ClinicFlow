from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, status, get_db
)
from models.cmh.immunization_model import ImmunizationModel
from schema.cmh.immunization_schema import ImmunizationCreateSchema, ImmunizationResponseSchema

router = APIRouter(prefix="/immunizations", tags=["Immunizations"])

# create immunization
@router.post("/", response_model = ImmunizationResponseSchema)
def create_immunization(
    immunization: ImmunizationCreateSchema,
    db: Session = Depends(get_db)
):
    new_immunization = ImmunizationModel(**immunization.model_dump())

    db.add(new_immunization)
    db.commit()
    db.refresh(new_immunization)

    return new_immunization

# get all immunization
@router.get("/", response_model = List[ImmunizationResponseSchema])
def get_all_immunizations(db: Session = Depends(get_db)):
    return db.query(ImmunizationModel).filter(ImmunizationModel.is_active == True).all()

# get immunization by id
@router.get("/{immunization_id}", response_model = ImmunizationResponseSchema)
def get_immunization(immunization_id: int, db: Session = Depends(get_db)):
    immunization = db.query(ImmunizationModel).filter(
        ImmunizationModel.immunization_id == immunization_id,
        ImmunizationModel.is_active == True
    ).first()

    if not immunization:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Immunization Record Not Found"
        )
    
    return immunization

# update immunization
@router.put("/{immunization_id}", response_model = ImmunizationResponseSchema)
def update_immunization(
    immunization_id: int,
    immunization_data: ImmunizationCreateSchema,
    db: Session = Depends(get_db)
):
    immunization = db.query(ImmunizationModel).filter(
        ImmunizationModel.immunization_id == immunization_id,
        ImmunizationModel.is_active == True
    ).first()

    if not immunization:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Immunization Record Not Found"
        )
    
    for key, value in immunization_data.model_dump(exclude_unset = True):
        setattr(immunization, key, value)

    db.commit()
    db.refresh(immunization)

    return immunization

# soft delete
@router.delete("/{immunization_id}")
def delete_immunization(immunization_id: int, db: Session = Depends(get_db)):
    immunization = db.query(ImmunizationModel).filter(
        ImmunizationModel.immunization_id == immunization_id,
        ImmunizationModel.is_active == True
    ).first()

    if not immunization:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Immunization Record Not Found"
        )
    
    immunization.is_active = False

    db.commit()
    return {
        "message": "Immunization record deleted successfully"
    }