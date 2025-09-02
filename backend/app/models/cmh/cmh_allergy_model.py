from lib.lib_import import (
    Base, Column, Integer, String, Enum, DateTime, 
    ForeignKey, Boolean, relationship, enum, datetime, timezone
)

class AllergySeverityEnum(str, enum.Enum):
    mild = "MILD"
    moderate = "MODERATE"
    severe = "SEVERE"

class AllergyStatusEnum(str, enum.Enum):
    active = "ACTIVE"
    inactive = "INACTIVE"

class MedicalAllergyModel(Base):
    __tablename__ = "medical_allergies"

    allergy_id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable = False, index = True)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable=False, index=True)
    substance = Column(String, nullable = False)
    reaction = Column(String, nullable = True)
    severity = Column(Enum(AllergySeverityEnum), nullable = True)
    status = Column(Enum(AllergyStatusEnum), default = AllergyStatusEnum.active)

    recorded_at = Column(DateTime, default = lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default = True)

    # relationships
    patient = relationship("PatientModel", back_populates = "allergies")
    doctor = relationship("DoctorModel", back_populates = "allergies")