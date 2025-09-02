from lib.lib_import import (
    APIRouter, Depends, HTTPException, Query, Session, Optional, List, get_db, datetime,
)
from models.cmh.cmh_allergy_model import MedicalAllergyModel
from models.cmh.medical_condition_model import MedicalConditionModel
from models.cmh.medication_model import MedicationStatementModel
from models.cmh.immunization_model import ImmunizationModel
from models.cmh.procedure_model import ProcedureModel
from models.cmh.vital_snapshot_model import VitalSnapshotModel
from models.cmh.medical_doc_model import MedicalDocumentModel
from models.cmh.encounter_note_model import EncounterNoteModel
from models.patient_model import PatientModel
from schema.cmh.timeline_schema import TimelineResponseSchema, TimelineEntrySchema

router = APIRouter(prefix="/cmh", tags=["CMH Timeline"])

@router.get("/{patient_id}/timeline", response_model=TimelineResponseSchema)
def get_patient_timeline(
    patient_id: int,
    db: Session = Depends(get_db),
    type: Optional[str] = Query(
        None,
        description="Filter by type (allergy, condition, medication, immunization, procedure, vital, encounter_note, document)"
    ),
    search: Optional[str] = Query(
        None,
        description="Keyword search across summaries (e.g., 'diabetes', 'aspirin')"
    ),
    start_date: Optional[datetime] = Query(
        None,
        description = "Filter events after this date (YYYY-MM-DD)"
    ),
    end_date: Optional[datetime] = Query(
        None,
        description = "Filter events before this date (YYYY-MM-DD)"
    ),
    limit: int = Query(50, ge=1, le=200, description="Limit number of records"),
    skip: int = Query(0, ge=0, description="Skip number of records for pagination")
):
    """Return chronological CMH Timeline for a patient, with filters and pagination"""

    patient = db.query(PatientModel).filter(PatientModel.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    timeline_entries: List[TimelineEntrySchema] = []

    def add_entry(date, type, summary, ref_id, doctor = None):
        if date:
            timeline_entries.append(TimelineEntrySchema(
                date = date,
                type = type,
                summary = summary,
                reference_id = ref_id,
                doctor_id = getattr(doctor, "doctor_id", None),
                doctor_name = f"{doctor.user.first_name} {doctor.user.last_name}".strip() if doctor and doctor.user else None
            ))

    # allergies
    if type is None or type == "allergy":
        allergies = db.query(MedicalAllergyModel).filter(MedicalAllergyModel.patient_id == patient_id).all()
        for a in allergies:
            add_entry(
                date=a.recorded_at,
                type="allergy",
                summary=f"Allergy recorded: {a.substance} ({a.severity})",
                reference_id=a.allergy_id
            )

    # conditions
    if type is None or type == "condition":
        conditions = db.query(MedicalConditionModel).filter(MedicalConditionModel.patient_id == patient_id).all()
        for c in conditions:
            add_entry(
                date=c.diagnosed_at,
                type="condition",
                summary=f"Condition diagnosed: {c.condition_name} ({c.status})",
                reference_id=c.condition_id
            )

    # medications
    if type is None or type == "medication":
        medications = db.query(MedicationStatementModel).filter(MedicationStatementModel.patient_id == patient_id).all()
        for m in medications:
            add_entry(
                date=m.start_date,
                type="medication",
                summary=f"Medication started: {m.medication_name}",
                reference_id=m.medication_id
            )

    # immunizations
    if type is None or type == "immunization":
        immunizations = db.query(ImmunizationModel).filter(ImmunizationModel.patient_id == patient_id).all()
        for i in immunizations:
            add_entry(
                date=i.date_administered,
                type="immunization",
                summary=f"Vaccine given: {i.vaccine_name}",
                reference_id=i.immunization_id
            )

    # procedures
    if type is None or type == "procedure":
        procedures = db.query(ProcedureModel).filter(ProcedureModel.patient_id == patient_id).all()
        for p in procedures:
            add_entry(
                date=p.performed_at,
                type="procedure",
                summary=f"Procedure performed: {p.procedure_name}",
                reference_id=p.procedure_id
            )

    # vitals
    if type is None or type == "vital":
        vitals = db.query(VitalSnapshotModel).filter(VitalSnapshotModel.patient_id == patient_id).all()
        for v in vitals:
            add_entry(
                date=v.recorded_at,
                type="vital",
                summary=f"Vitals recorded: BP {v.blood_pressure}, HR {v.heart_rate}, BMI {v.bmi}",
                reference_id=v.vital_id
            )

    # encounter notes
    if type is None or type == "encounter_note":
        notes = db.query(EncounterNoteModel).filter(EncounterNoteModel.patient_id == patient_id).all()
        for n in notes:
            add_entry(
                date=n.recorded_at,
                type="encounter_note",
                summary=f"Encounter note: {n.note_title}",
                reference_id=n.note_id
            )

    # documents
    if type is None or type == "document":
        docs = db.query(MedicalDocumentModel).filter(MedicalDocumentModel.patient_id == patient_id).all()
        for d in docs:
            add_entry(
                date=d.uploaded_at,
                type="document",
                summary=f"Document uploaded: {d.file_name}",
                reference_id=d.document_id
            )

    # sort all entries by date (latest first)
    timeline_entries.sort(key=lambda x: x.date, reverse=True)

    # search filter
    if search:
        search_lower = search.lower()
        timeline_entries = [entry for entry in timeline_entries if search_lower in entry.summary.lower()]

    # date range filter
    if start_date:
        timeline_entries = [entry for entry in timeline_entries if entry.date >= start_date]
    if end_date:
        timeline_entries = [entry for entry in timeline_entries if entry.date <= end_date]

    # apply pagination
    paginated_entries = timeline_entries[skip: skip + limit]

    return TimelineResponseSchema(
        patient_id=patient.patient_id,
        timeline=paginated_entries
    )
