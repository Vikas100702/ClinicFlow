from lib.lib_import import (
    FastAPI, CORSMiddleware, appointments, doctor_availability, dashboard, forgot_password,
    prescriptions, lab_orders, auth, registration, allergies, conditions, medication,
    immunization, procedures, encounter_notes, medical_doc, vitals, summary
)

app = FastAPI(title="ClinicFlow APP", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)  

app.include_router(registration.router)
app.include_router(auth.router)
app.include_router(appointments.router)
app.include_router(doctor_availability.router)
app.include_router(dashboard.router)
app.include_router(forgot_password.router)
app.include_router(prescriptions.router)
app.include_router(lab_orders.router)
app.include_router(allergies.router)
app.include_router(conditions.router)
app.include_router(medication.router)
app.include_router(immunization.router)
app.include_router(procedures.router)
app.include_router(encounter_notes.router)
app.include_router(medical_doc.router)
app.include_router(vitals.router)
app.include_router(summary.router)