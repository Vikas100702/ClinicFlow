from app.models.models import Base, Column, Integer, String, ForeignKey, relationship


class PatientModel(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    address = Column(String(255), nullable=True)

    user = relationship("UserModel", backref="patient_profile")
