from lib.lib_import import Base, Column, Integer, String, ForeignKey, relationship

class DoctorModel(Base):
    __tablename__ = "doctors"

    doc_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    specialization = Column(String(100), nullable=False)
    qualification = Column(String(100), nullable=False)
    experience = Column(String(50), nullable=True)
    bio = Column(String(255), nullable=True)
    available_days = Column(String(100), nullable=True)

    # relationships
    user = relationship("UserModel", backref="doctor_profile")
    appointments = relationship("AppointmentModel", back_populates = "doctor", cascade = "all, delete-orphan")
    availability = relationship("DoctorAvailabilityModel", back_populates = "doctor", cascade = "all, delete-orphan")
    prescription = relationship("PrescriptionModel", back_populates = "doctor")
    allergies = relationship("MedicalAllergyModel", back_populates="doctor", cascade="all, delete-orphan")
    conditions = relationship("MedicalConditionModel", back_populates="doctor")
    documents = relationship("MedicalDocumentModel", back_populates="doctor", cascade="all, delete-orphan")
    medications = relationship("MedicationStatementModel", back_populates="doctor")
    immunizations = relationship("ImmunizationModel", back_populates="doctor")
    procedures = relationship("ProcedureModel", back_populates="doctor")
    encounter_notes = relationship("EncounterNoteModel", back_populates="doctor")
    vitals = relationship("VitalSnapshotModel", back_populates="doctor", cascade="all, delete-orphan")
