# ClinicFlow Backend

A comprehensive healthcare management system built with FastAPI and SQLAlchemy. This system provides APIs for managing patients, doctors, appointments, and complete medical records.

## Features

### Core Functionality
- **User Management**: Registration, authentication, and role-based access control
- **Appointment System**: Booking, scheduling, and availability management
- **Patient Dashboard**: View doctors, appointments, and medical history
- **Doctor Dashboard**: Manage appointments, patients, and medical records

### Complete Medical History (CMH)
- **Allergies**: Track patient allergies with severity levels
- **Medical Conditions**: Diagnose and monitor chronic conditions
- **Medications**: Manage current and historical medication records
- **Immunizations**: Track vaccination history and schedules
- **Procedures**: Record medical procedures and their status
- **Vital Signs**: Monitor height, weight, BMI, blood pressure, etc.
- **Encounter Notes**: Clinical notes and observations
- **Medical Documents**: Upload and manage medical files
- **Timeline**: Chronological view of all medical events
- **Summary**: Comprehensive patient medical overview

### Additional Features
- **Prescriptions**: Digital prescription management
- **Lab Orders**: Laboratory test ordering and results
- **Password Recovery**: Secure password reset functionality
- **File Uploads**: Support for medical documents and lab results

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy ORM (PostgreSQL/MySQL/SQLite compatible)
- **Authentication**: JWT tokens with role-based access
- **Password Security**: bcrypt hashing
- **Validation**: Pydantic schemas
- **File Handling**: Local file storage for documents

## Project Structure

```
backend/app/
├── main.py                 # FastAPI application entry point
├── core/                   # Core configuration and utilities
│   ├── config.py          # Environment configuration
│   ├── dependency.py      # Authentication dependencies
│   ├── jwt.py            # JWT token handling
│   ├── roles.py          # Role-based access control
│   └── security.py       # Password hashing utilities
├── lib/
│   └── lib_import.py     # Centralized imports
├── models/               # SQLAlchemy database models
│   ├── user_role_model.py
│   ├── patient_model.py
│   ├── doctor_model.py
│   ├── appointment_model.py
│   ├── prescription_model.py
│   ├── lab_order_model.py
│   ├── doctor_availability_model.py
│   └── cmh/             # Complete Medical History models
│       ├── cmh_allergy_model.py
│       ├── medical_condition_model.py
│       ├── medication_model.py
│       ├── immunization_model.py
│       ├── procedure_model.py
│       ├── vital_snapshot_model.py
│       ├── encounter_note_model.py
│       └── medical_doc_model.py
├── routes/              # API route handlers
│   ├── registration.py
│   ├── auth.py
│   ├── appointments.py
│   ├── dashboard.py
│   ├── prescriptions.py
│   ├── lab_orders.py
│   ├── forgot_password.py
│   ├── doctor_availability.py
│   └── cmh/            # Complete Medical History routes
│       ├── allergies.py
│       ├── conditions.py
│       ├── medication.py
│       ├── immunization.py
│       ├── procedures.py
│       ├── vitals.py
│       ├── encounter_notes.py
│       ├── medical_doc.py
│       ├── summary.py
│       └── timeline.py
├── schema/             # Pydantic request/response schemas
│   ├── user_schema.py
│   ├── auth_schema.py
│   ├── patient_schema.py
│   ├── doctor_schema.py
│   ├── appointment_schema.py
│   ├── prescription_schema.py
│   ├── lab_order_schema.py
│   ├── common_types.py
│   └── cmh/           # CMH schemas
│       ├── allergy_schema.py
│       ├── medical_condition_schema.py
│       ├── medication_schema.py
│       ├── immunization_schema.py
│       ├── procedure_schema.py
│       ├── vital_snapshot_schema.py
│       ├── encounter_note_schema.py
│       ├── medical_doc_schema.py
│       ├── cmh_summary_schema.py
│       └── timeline_schema.py
└── util/
    └── auth.py        # Authentication utilities
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd clinicflow/backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-multipart
   pip install passlib[bcrypt] pyjwt python-jose[cryptography] pydantic[email]
   ```

4. **Environment Configuration**:
   Create a `.env` file in the app directory:
   ```env
   SECRET_KEY=your_super_secret_key_here
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   DATABASE_URL=postgresql://username:password@localhost/clinicflow
   ```

5. **Database Setup**:
   ```python
   # Create database tables
   from database.database import engine, Base
   Base.metadata.create_all(bind=engine)
   ```

6. **Run the application**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## User Roles

### ADMIN
- Full system access
- Upload lab results
- Manage all users and data

### DOCTOR
- Create and manage patient records
- View patient medical history
- Create prescriptions and lab orders
- Schedule appointments
- Update medical information

### PATIENT
- View personal medical history
- Book appointments with doctors
- Access prescriptions and lab results
- Update personal information

## Key API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/protected` - Protected route example

### Registration
- `POST /register/user` - Register new user
- `POST /register/doctor` - Register doctor profile
- `POST /register/patient` - Register patient profile
- `GET /register/users` - List all users

### Appointments
- `POST /appointments/` - Create appointment
- `GET /appointments/{id}` - Get appointment details
- `DELETE /appointments/{id}` - Cancel appointment

### Dashboard
- `GET /dashboard/patient` - Patient dashboard
- `GET /dashboard/doctor` - Doctor dashboard

### Complete Medical History
- `GET /cmh/{patient_id}/summary` - Patient medical summary
- `GET /cmh/{patient_id}/timeline` - Medical timeline
- `POST /allergies/` - Add allergy
- `POST /conditions/` - Add medical condition
- `POST /medications/` - Add medication
- `POST /immunizations/` - Add immunization
- `POST /procedures/` - Add procedure
- `POST /vitals/` - Record vital signs
- `POST /encounter-notes/` - Add clinical notes
- `POST /documents/` - Upload medical documents

### Prescriptions & Lab Orders
- `POST /prescriptions/` - Create prescription
- `GET /prescriptions/patient/{id}` - Get patient prescriptions
- `POST /lab-orders/` - Create lab order
- `POST /lab-orders/{id}/upload` - Upload lab results

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Different permissions for different user types
- **Password Security**: bcrypt hashing with secure validation rules
- **Input Validation**: Comprehensive Pydantic schema validation
- **CORS Configuration**: Configurable cross-origin resource sharing

## Database Features

- **Soft Deletes**: Most records use `is_active` flags instead of hard deletion
- **Audit Trails**: Created/updated timestamps on records
- **Referential Integrity**: Proper foreign key relationships
- **Data Validation**: Database-level constraints and checks
- **Auto-calculated Fields**: BMI automatically calculated from height/weight

## Error Handling

The API provides structured error responses:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

Common HTTP status codes used:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error

## File Upload Support

The system supports file uploads for:
- Medical documents (PDF, images, etc.)
- Lab results
- Medical imaging files

Files are stored locally in the `uploads/` directory with proper organization.

## Development Notes

### Adding New Features
1. Create database model in `models/`
2. Add Pydantic schemas in `schema/`
3. Implement routes in `routes/`
4. Update `main.py` to include new router
5. Add imports to `lib/lib_import.py` if needed

### Database Migrations
Consider using Alembic for database migrations in production:
```bash
pip install alembic
alembic init alembic
```

### Testing
Implement tests using pytest:
```bash
pip install pytest pytest-asyncio httpx
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support or questions, please create an issue in the repository or contact the development team.

---

**ClinicFlow** - Streamlining healthcare management through technology.