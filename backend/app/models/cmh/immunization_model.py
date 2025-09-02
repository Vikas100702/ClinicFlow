from lib.lib_import import (
    Base, Column, Integer, String, Enum, DateTime, enum,
    ForeignKey, Boolean, relationship, datetime, timezone
)

class ImmunizationStatusEnum(str, enum.Enum):
    completed = "COMPLETED"
    pending = "PENDING"
    cancelled = "CANCELLED"

class ImmunizationModel(Base):
    __tablename__ = "immuniztions"

    immunization_id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable=True)

    vaccine_name = Column(String(100), nullable=False)
    manufacturer = Column(String(100), nullable=True)
    lot_number = Column(String(100), nullable=True)
    dose_number = Column(Integer, nullable=True)  # e.g. 1st dose, 2nd dose
    administered_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    next_due_date = Column(DateTime, nullable=True)

    route = Column(String(50), nullable=True)      # e.g. Intramuscular, Oral
    site = Column(String(50), nullable=True)       # e.g. Left Arm, Right Arm
    notes = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)

    # relationships
    patient = relationship("PatientModel", back_populates="immunizations")
    doctor = relationship("DoctorModel", back_populates="immunizations")
