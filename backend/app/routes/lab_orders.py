from lib.lib_import import (
    APIRouter, Session, Depends, UploadFile, File, HTTPException, 
    status, get_db, role_checker, List, os, uuid
)
from models.lab_order_model import LabOrderModel, LabOrderStatusEnum
from schema.lab_order_schema import LaborderCreateSchema, LabOrderResponseSchema

router = APIRouter(prefix = "/lab-orders", tags = ["Lab Orders"])

UPLOAD_DIR = "./uploads/labs"

os.makedirs(UPLOAD_DIR, exist_ok = True)

@router.post("/", response_model = LabOrderResponseSchema, dependencies = [Depends(role_checker("DOCTOR"))])
def create_lab_order(lab_order: LaborderCreateSchema, db: Session = Depends(get_db)):
    new_order = LabOrderModel(**lab_order.model_dump())

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/", response_model = List[LabOrderResponseSchema])
def list_lab_orders(patient_id: int, db: Session = Depends(get_db)):
    return db.query(LabOrderModel).join(LabOrderModel.appointment)\
            .filter(LabOrderModel.appointment.has(patient_id = patient_id)\
        ).all()

@router.post("{id}/upload", response_model = LabOrderResponseSchema, dependencies = [Depends(role_checker("ADMIN"))])
def upload_result(lab_order_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    lab_order = db.query(LabOrderModel).filter(LabOrderModel.lab_order_id == lab_order_id).first()

    if not lab_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab order not found"
        )
    
    # save file
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    lab_order.result_file_path = file_path
    lab_order.status = LabOrderStatusEnum.COMPLETED

    db.commit()
    db.refresh(lab_order)

    return lab_order
