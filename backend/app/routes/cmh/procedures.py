from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, List, status, get_db,

)
from schema.procedure_schema import ProcedureCreateSchema, ProcedureResponseSchema, ProcedureStatusEnum, ProcedureUpdateSchema
from models.cmh.procedure_model import ProcedureModel

router = APIRouter(prefix="/procedures", tags=["Medical Procedures"])

# create Procedure
@router.post("/", response_model=ProcedureResponseSchema)
def create_procedure(procedure: ProcedureCreateSchema, db: Session = Depends(get_db)):
    new_procedure = ProcedureModel(**procedure.model_dump())
    db.add(new_procedure)
    db.commit()
    db.refresh(new_procedure)
    return new_procedure

# get all Procedures
@router.get("/", response_model=List[ProcedureResponseSchema])
def get_procedures(db: Session = Depends(get_db)):
    return db.query(ProcedureModel).filter(ProcedureModel.is_active == True).all()

# get single Procedure
@router.get("/{procedure_id}", response_model=ProcedureResponseSchema)
def get_procedure(procedure_id: int, db: Session = Depends(get_db)):
    procedure = db.query(ProcedureModel).filter(ProcedureModel.procedure_id == procedure_id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    return procedure

# update Procedure
@router.put("/{procedure_id}", response_model=ProcedureResponseSchema)
def update_procedure(procedure_id: int, procedure_data: ProcedureUpdateSchema, db: Session = Depends(get_db)):
    procedure = db.query(ProcedureModel).filter(ProcedureModel.procedure_id == procedure_id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")

    for key, value in procedure_data.model_dump(exclude_unset=True).items():
        setattr(procedure, key, value)

    db.commit()
    db.refresh(procedure)
    return procedure

# soft Delete Procedure
@router.delete("/{procedure_id}")
def delete_procedure(procedure_id: int, db: Session = Depends(get_db)):
    procedure = db.query(ProcedureModel).filter(ProcedureModel.procedure_id == procedure_id).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")

    procedure.is_active = False
    db.commit()
    return {"detail": "Procedure soft deleted successfully"}
