from lib.lib_import import (
    Base, Column, Integer, String, ForeignKey,
    DateTime, Text, relationship, func
)

class PrescriptionModel(Base):
    __tablename__ = "prescription"

    presc_id = Column(
        Integer, primary_key = True, index = True,
        autoincrement = True
    )
    appointment_id = Column(
        Integer, ForeignKey("appointments.appointment_id"),
        nullable = False
    )
    doctor_id = Column(
        Integer, ForeignKey("doctors.doc_id"),
        nullable = False
    )
    patient_id = Column(
        Integer, ForeignKey("patients.patient_id"),
        nullable = False
    )

    medicines = Column(Text, nullable = False)
    notes = Column(Text, nullable = True)

    created_at = Column(DateTime(timezone = True), server_default = func.now())

    # Relationships
    appointment = relationship("AppointmentModel", back_populates = "prescription")
    doctor = relationship("DoctorModel", back_populates = "prescription")
    patient = relationship("PatientModel", back_populates = "prescription")