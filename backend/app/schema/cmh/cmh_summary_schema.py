from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class CMHSummarySchema(BaseModel):
    patient_id: int
    patient_name: str

    allergies: List[str] = []
    conditions: List[str] = []
    medications: List[str] = []
    immunizations: List[str] = []
    procedures: List[str] = []
    encounter_notes: List[str] = []

    last_vitals: Optional[Dict[str, Any]] = None
    recent_docs: List[str] = []

    class Config:
        from_attributes = True