from lib.lib_import import (
    Column, BigInteger, SmallInteger, Time, Boolean, ForeignKey, 
    DateTime, CheckConstraint, relationship, func, Base
)

class DoctorAvailabilityModel(Base):
    __tablename__ = "doctor_availability"

    availability_id = Column(BigInteger, primary_key = True, autoincrement = True)
    doctor_id = Column(BigInteger , ForeignKey("doctors.doc_id", ondelete = "CASCADE"), nullable = False)

    day_of_week = Column(SmallInteger, nullable = False) # 0 = Monday....6 = Sunday
    start_time = Column(Time, nullable = False)
    end_time = Column(Time, nullable = False)
    is_active = Column(Boolean, nullable = False, default = True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # relationships
    doctor = relationship("DoctorModel", back_populates = "availability")

    __table_args__ = (
        CheckConstraint("end_time > start_time", name="check_available_range"),
    )
