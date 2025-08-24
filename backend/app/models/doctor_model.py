from app.models.models import Base, Column, Integer, String, ForeignKey, relationship


class DoctorModel(Base):
    __tablename__ = "doctors"

    doc_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    specialization = Column(String(100), nullable=False)
    qualification = Column(String(100), nullable=False)
    experience = Column(String(50), nullable=True)
    bio = Column(String(255), nullable=True)
    available_days = Column(String(100), nullable=True)

    user = relationship("UserModel", backref="doctor_profile")
