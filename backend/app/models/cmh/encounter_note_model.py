from lib.lib_import import (
    Base, Column, Integer, String, Text, DateTime,
    ForeignKey, Boolean, relationship, datetime, timezone
)

class EncounterNoteModel(Base):
    __tablename__ = "encounter_notes"

    note_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable=False)

    title = Column(String(255), nullable=False)  # e.g., "Follow-up Visit"
    content = Column(Text, nullable=False)       # the actual note body

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    is_active = Column(Boolean, default=True)

    # Relationships
    patient = relationship("PatientModel", back_populates="encounter_notes")
    doctor = relationship("DoctorModel", back_populates="encounter_notes")
