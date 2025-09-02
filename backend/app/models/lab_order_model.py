from lib.lib_import import (
    Column, Integer, String, Enum, ForeignKey, 
    enum, DateTime, relationship, datetime, timezone, Base
)

class LabOrderStatusEnum(enum.Enum):
    ORDERED = "ordered"
    SAMPLE_COLLECTED = "sample_collected"
    COMPLETED = "completed"

class LabOrderModel(Base):
    __tablename__ = "lab_orders"

    lab_order_id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id"), nullable = False)
    test_name = Column(String, nullable = False)
    notes = Column(String, nullable = False)
    status = Column(Enum(LabOrderStatusEnum), default = LabOrderStatusEnum.ORDERED)
    result_file_path = Column(String, nullable = True)
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc))

    # relationships
    appointment = relationship("AppointmentModel", back_populates = "lab_order")
