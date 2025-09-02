import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from database.database import Base
from dotenv import load_dotenv
from models import (
    user_role_model, patient_model, doctor_model, 
    appointment_model, doctor_availability_model,
    prescription_model, lab_order_model
)

from models.cmh import (
    cmh_allergy_model, medical_condition_model, medication_model,
    immunization_model, procedure_model, encounter_note_model,
    medical_doc_model, vital_snapshot_model
)

load_dotenv()

User = user_role_model.UserModel
Doctor = doctor_model.DoctorModel
Patient = patient_model.PatientModel
Appointment = appointment_model.AppointmentModel
Doctor_Availability = doctor_availability_model.DoctorAvailabilityModel
Prescription = prescription_model.PrescriptionModel
Lab_Order = lab_order_model.LabOrderModel
CMH_Allergy = cmh_allergy_model.MedicalAllergyModel
Medical_Condition = medical_condition_model.MedicalConditionModel
Medication_Statement = medication_model.MedicationStatementModel
Immunization = immunization_model.ImmunizationModel
Procedure = procedure_model.ProcedureModel
Vital_Snapshot = vital_snapshot_model.VitalSnapshotModel
Encounter_Notes = encounter_note_model.EncounterNoteModel
Medical_Doc = medical_doc_model.MedicalDocumentModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

DATABASE_URL = os.getenv('DB_URL')
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
