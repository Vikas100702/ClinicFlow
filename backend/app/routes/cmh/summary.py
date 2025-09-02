from lib.lib_import import (
    APIRouter, Depends, HTTPException, Session, get_db, status
)
from models.patient_model import PatientModel
from models.cmh.cmh_allergy_model import MedicalAllergyModel
from models.cmh.medical_condition_model import MedicalConditionModel
from models.cmh.medication_model import MedicationStatementModel
from models.cmh.immunization_model import ImmunizationModel
from models.cmh.procedure_model import ProcedureModel
from models.cmh.encounter_note_model import EncounterNoteModel
from models.cmh.vital_snapshot_model import VitalSnapshotModel
from models.cmh.medical_doc_model import MedicalDocumentModel
from schema.cmh.cmh_summary_schema import CMHSummarySchema

router = APIRouter(prefix = "/cmh", tags = ["CMH Summary"])

@router.get("/{patient_id}/summary", response_model = CMHSummarySchema)
def get_patient_summary(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.patient_id == patient_id).first()

    if not patient:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "patient Not Found"
        )
    
    user = patient.user
    patient_name = f"{user.first_name} {user.last_name}" if user else "Unknown"

    # active allergies
    allergies = db.query(MedicalAllergyModel).filter(
        MedicalAllergyModel.patient_id == patient_id,
        MedicalAllergyModel.is_active == True
    ).all()

    # active conditions
    conditions = db.query(MedicalConditionModel).filter(
        MedicalConditionModel.patient_id == patient_id,
        MedicalConditionModel.is_active == True
    ).all()

    # active medications
    medications = db.query(MedicationStatementModel).filter(
        MedicationStatementModel.patient_id == patient_id,
        MedicationStatementModel.is_active == True
    ).all()

    # immunization history
    immunizations = db.query(ImmunizationModel).filter(
        ImmunizationModel.patient_id == patient_id
    ).all()

    # recent procedures
    procedures = db.query(ProcedureModel).filter(
        ProcedureModel.patient_id == patient_id,
        ProcedureModel.is_active == True
    ).all()

    #encounter notes
    encounter_notes = db.query(EncounterNoteModel).filter(
        EncounterNoteModel.patient_id == patient_id,
        EncounterNoteModel.is_active == True
    ).order_by(EncounterNoteModel.created_at.desc()).limit(10).all()
    
    # latest vital snapshot
    last_vitals = db.query(VitalSnapshotModel).filter(
        VitalSnapshotModel.patient_id == patient_id
    ).order_by(VitalSnapshotModel.recorded_at.desc()).first()

    # recent uploaded docs
    documents = db.query(MedicalDocumentModel).filter(
        MedicalDocumentModel.patient_id == patient_id,
        MedicalDocumentModel.is_active == True
    ).order_by(MedicalDocumentModel.uploaded_at.desc()).limit(10).all()

    return CMHSummarySchema(
        patient_id = patient.patient_id,
        patient_name = patient_name,

        allergies = [a.substance for a in allergies],
        conditions = [c.condition_name for c in conditions],
        medications = [m.medication_name for m in medications],
        immunizations = [i.vaccine_name for i in immunizations],
        procedures = [p.procedure_name for p in procedures],
        encounter_notes = [e.title for e in encounter_notes],
        last_vitals = {
            "height_cm": last_vitals.height_cm,
            "weight_kg": last_vitals.weight_kg,
            "bmi": last_vitals.bmi,
            "blood_pressure": last_vitals.blood_pressure,
            "heart_rate": last_vitals.heart_rate,
            "respiratory_rate": last_vitals.respiratory_rate,
            "temprature": last_vitals.temperature,
            "oxygen_saturation": last_vitals.oxygen_saturation,
            "recorded_at": last_vitals.recorded_at
        } if last_vitals else None,
        recent_docs = [d.title for d in documents]
    )