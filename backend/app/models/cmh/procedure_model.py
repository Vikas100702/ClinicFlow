from lib.lib_import import (
    Base, Column, Integer, String, Enum, DateTime,
    ForeignKey, Boolean, relationship, datetime, timezone, enum
)

class ProcedureStatusEnum(str, enum.Enum):
    scheduled = "SCHEDULED"
    completed = "COMPLETED"
    cancelled = "CANCELLED"

class ProcedureModel(Base):
    __tablename__ = "medical_procedures"

    procedure_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable=True)

    procedure_name = Column(String, nullable=False)  # e.g., Appendectomy
    description = Column(String, nullable=True)
    status = Column(Enum(ProcedureStatusEnum), default=ProcedureStatusEnum.scheduled)

    performed_at = Column(DateTime, nullable=True)  # actual date of procedure
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    is_active = Column(Boolean, default=True)

    # relationships
    patient = relationship("PatientModel", back_populates="procedures")
    doctor = relationship("DoctorModel", back_populates="procedures")
