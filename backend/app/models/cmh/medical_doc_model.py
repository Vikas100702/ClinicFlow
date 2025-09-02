from lib.lib_import import (
    Base, Column, Integer, String, DateTime,
    ForeignKey, Boolean, relationship, datetime, timezone
)

class MedicalDocumentModel(Base):
    __tablename__ = "medical_documents"

    document_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable=True)

    title = Column(String(255), nullable=False)  # e.g., "MRI Scan Report"
    file_path = Column(String(500), nullable=False)  # path to uploaded file
    file_type = Column(String(50), nullable=False)   # pdf, jpg, png, etc.

    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    # Relationships
    patient = relationship("PatientModel", back_populates="documents")
    doctor = relationship("DoctorModel", back_populates="documents")
