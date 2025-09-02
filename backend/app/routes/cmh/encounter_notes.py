from lib.lib_import import APIRouter, Depends, HTTPException, Session, List, get_db
from schema.cmh.encounter_note_schema import (
    EncounterNoteCreateSchema, EncounterNoteResponseSchema, EncounterNoteUpdateSchema
)
from models.cmh.encounter_note_model import EncounterNoteModel

router = APIRouter(prefix="/encounter-notes", tags=["Encounter Notes"])

# create
@router.post("/", response_model=EncounterNoteResponseSchema)
def create_note(note: EncounterNoteCreateSchema, db: Session = Depends(get_db)):
    new_note = EncounterNoteModel(**note.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# get all notes
@router.get("/", response_model=List[EncounterNoteResponseSchema])
def get_all_notes(db: Session = Depends(get_db)):
    return db.query(EncounterNoteModel).all()

# get note by id
@router.get("/{note_id}", response_model=EncounterNoteResponseSchema)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(EncounterNoteModel).filter(EncounterNoteModel.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# update
@router.put("/{note_id}", response_model=EncounterNoteResponseSchema)
def update_note(
    note_id: int,
    note_data: EncounterNoteUpdateSchema,
    db: Session = Depends(get_db)
):
    note = db.query(EncounterNoteModel).filter(EncounterNoteModel.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    for key, value in note_data.model_dump(exclude_unset=True).items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)
    return note

# soft delete
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(EncounterNoteModel).filter(EncounterNoteModel.note_id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.is_active = False
    db.commit()
    return {"message": "Encounter note deleted successfully"}
