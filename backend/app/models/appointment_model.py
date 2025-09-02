from lib.lib_import import (
    Column, BigInteger, String, Enum, ForeignKey, relationship, CheckConstraint,
    UniqueConstraint, func, Base, enum, DateTime, datetime, timezone
)

class AppointmentStatus(str, enum.Enum):
    booked = "BOOKED"
    confirmed = "CONFIRMED"
    completed = "COMPLETED"
    cancelled = "CANCELLED"

class AppointmentModel(Base):
    __tablename__ = "appointments"

    appointment_id = Column(BigInteger, primary_key = True, autoincrement = True)
    patient_id = Column(BigInteger, ForeignKey("patients.patient_id", ondelete = "CASCADE"), nullable = False)
    doctor_id = Column(BigInteger, ForeignKey("doctors.doc_id", ondelete = "CASCADE"), nullable = False)

    start_time = Column(DateTime(timezone = True), nullable = False)
    end_time = Column(DateTime(timezone = True), nullable = False)
    disease = Column(String(1000))
    status = Column(Enum(AppointmentStatus), nullable = False, default = AppointmentStatus.booked)

    created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    updated_at = Column(DateTime(timezone = True), server_default = func.now(), onupdate = func.now(), nullable = False)

    # Relationships
    patient = relationship("PatientModel", back_populates = "appointments")
    doctor = relationship("DoctorModel", back_populates = "appointments")
    prescription = relationship("PrescriptionModel", back_populates = "appointment")
    lab_order = relationship("LabOrderModel", back_populates = "appointment")

    __table_args__ = (
        CheckConstraint("end_time > start_time", name = "check_time_range"),
        UniqueConstraint("doctor_id", "start_time", "end_time", name = "uq_doc_timeslot")
    )