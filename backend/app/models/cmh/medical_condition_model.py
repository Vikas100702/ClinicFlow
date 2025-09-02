from lib.lib_import import (
    Base, Column, Integer, String, Enum, DateTime, enum,
    ForeignKey, Boolean, relationship, datetime, timezone
)

class ConditionStatusEnum(str, enum.Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"
    resolved = "RESOLVED"

class MedicalConditionModel(Base):
    __tablename__ = "medical_conditions"

    condition_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable = False)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable = True)

    condition_name = Column(String, nullable = False)  # e.g., Diabetes, Hypertension
    description = Column(String, nullable=True)
    status = Column(Enum(ConditionStatusEnum), default = ConditionStatusEnum.active)

    diagnosed = Column(DateTime, default = lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default = True)

    # relationships
    patient = relationship("PatientModel", back_populates = "conditions")
    doctor = relationship("DoctorModel", back_populates = "conditions")