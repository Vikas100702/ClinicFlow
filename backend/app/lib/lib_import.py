import os, enum, re, uuid

from enum import Enum
from uuid import uuid4

# typing
from typing import List, Optional, Annotated

# pydantic
from pydantic import (
    BaseModel, EmailStr, StringConstraints, field_validator
)

# fastapi
from fastapi import (
    APIRouter, FastAPI, Depends, HTTPException, Query,
    status, UploadFile, File
)
from fastapi.middleware.cors import CORSMiddleware

# passlib
from passlib.hash import bcrypt

# dotenv
from dotenv import load_dotenv

# sqlalchemy
from sqlalchemy.orm import Session, relationship, validates, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, BigInteger, SmallInteger, Float, Boolean,
    String, Enum, DateTime, ForeignKey, UniqueConstraint, CheckConstraint,
    Time, Text, create_engine
)

# datetime
from datetime import datetime, timezone, time, timedelta

# database
from database.database import Base, get_db

# core
from core.dependency import get_current_user
from core.jwt import create_access_token, decode_access_token
from core.roles import role_checker
from core.security import hash_password, verify_password

# routes
from routes import (
    appointments, auth, dashboard, doctor_availability, forgot_password,
    lab_orders, prescriptions, registration
)

# routes/cmh
from routes.cmh import (
    allergies, conditions, encounter_notes, immunization, medical_doc, medication,
    procedures, summary, timline, vitals
)