from lib.lib_import import (
    Base, Column, Integer, String, Float, DateTime, validates,
    ForeignKey, Boolean, relationship, datetime, timezone
)

class VitalSnapshotModel(Base):
    __tablename__ = "vital_snapshots"

    vital_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doc_id"), nullable=True)

    # vitals
    height_cm = Column(Float, nullable = True)
    weight_kg = Column(Float, nullable = True)
    bmi = Column(Float, nullable = True)

    blood_pressure = Column(String, nullable=True)   # e.g., "120/80"
    heart_rate = Column(Integer, nullable=True)      # BPM
    respiratory_rate = Column(Integer, nullable=True)
    temperature = Column(Float, nullable=True)       # °C
    oxygen_saturation = Column(Float, nullable=True) # %

    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    # relationships
    patient = relationship("PatientModel", back_populates="vitals")
    doctor = relationship("DoctorModel", back_populates="vitals")

    # auto-calculate bmi when values are set
    @validates("height_cm", "weight_kg")
    def calculate_bmi(self, key, value):
        setattr(self, key, value)

        if self.height_cm and self.weight_kg:
            try:
                self.bmi = round(
                    self.weight_kg / ((self.height_cm / 100)**2), 2
                )
            except ZeroDivisionError:
                self.bmi = None
        else:
            self.bmi = None

        return value 
