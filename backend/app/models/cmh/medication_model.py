from lib.lib_import import (
    Base, Column, Integer, String, Enum, DateTime, enum,
    ForeignKey, Boolean, relationship, datetime, timezone
)

class MedicationStatementModel(Base):
    __tablename__ = "medication_model"

    medication_id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable=True)

    medication_name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=True)
    frequency = Column(String(100), nullable=True)
    route = Column(String(100), nullable=True)  # e.g. Oral, IV, IM
    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime, nullable=True)
    instructions = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # relationships
    patient = relationship("PatientModel", back_populates="medications")
    doctor = relationship("DoctorModel", back_populates="medications")