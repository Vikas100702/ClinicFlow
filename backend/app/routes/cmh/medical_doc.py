from lib.lib_import import (
    APIRouter, Depends, HTTPException, UploadFile, File, 
    List, status, os, uuid4, get_db, Session
)
from models.cmh.medical_doc_model import MedicalDocumentModel
from schema.cmh.medical_doc_schema import MedicalDocumentResponseSchema

UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/documents", tags=["Medical Documents"])

# upload document
@router.post("/", response_model=MedicalDocumentResponseSchema)
async def upload_document(
    patient_id: int,
    doctor_id: int = None,
    title: str = "Medical Document",
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # save file
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    new_doc = MedicalDocumentModel(
        patient_id=patient_id,
        doctor_id=doctor_id,
        title=title,
        file_path=file_path,
        file_type=ext
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

# get all documents
@router.get("/", response_model=List[MedicalDocumentResponseSchema])
def get_all_documents(db: Session = Depends(get_db)):
    return db.query(MedicalDocumentModel).all()

# get document by id
@router.get("/{document_id}", response_model=MedicalDocumentResponseSchema)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(MedicalDocumentModel).filter(MedicalDocumentModel.document_id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Document not found"
        )
    return doc

# soft delete
@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(MedicalDocumentModel).filter(MedicalDocumentModel.document_id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail="Document not found"
        )

    doc.is_active = False
    db.commit()
    return {
        "message": "Document deleted successfully"
    }
