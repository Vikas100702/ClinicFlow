from lib.lib_import import Base, Column, Integer, String, ForeignKey, relationship

class PatientModel(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    address = Column(String(255), nullable=True)

    # relationships
    user = relationship("UserModel", backref="patient_profile")
    appointments = relationship("AppointmentModel", back_populates = "patient", cascade = "all, delete-orphan")
    prescription = relationship("PrescriptionModel", back_populates = "patient")
    allergies = relationship("MedicalAllergyModel", back_populates="patient", cascade="all, delete-orphan")
    conditions = relationship("MedicalConditionModel", back_populates="patient")
    documents = relationship("MedicalDocumentModel", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("MedicationStatementModel", back_populates="patient")
    immunizations = relationship("ImmunizationModel", back_populates="patient")
    procedures = relationship("ProcedureModel", back_populates="patient")
    encounter_notes = relationship("EncounterNoteModel", back_populates="patient")
    vitals = relationship("VitalSnapshotModel", back_populates="patient", cascade="all, delete-orphan")
