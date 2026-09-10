import os
import sys

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "app")
os.makedirs(os.path.join(base_dir, "routers"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "ml"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)

# 1. database.py
with open(os.path.join(base_dir, "database.py"), "w") as f:
    f.write('''import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cybertrace.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

# 2. models.py
with open(os.path.join(base_dir, "models.py"), "w") as f:
    f.write('''import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from .database import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(50), unique=True, index=True, nullable=False)
    fraud_type = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    victim_name = Column(String(150), default="Anonymous Complainant")
    victim_phone = Column(String(50), default="+91 98XXX XXXXX")
    victim_location = Column(String(150), default="Bengaluru, Karnataka")
    status = Column(String(50), default="NEW")
    risk_level = Column(String(20), default="MEDIUM")
    risk_score = Column(Float, default=50.0)
    predicted_location_id = Column(String(50), default="")
    predicted_atm_name = Column(String(150), default="")
    predicted_time_window = Column(String(100), default="")
    predicted_amount = Column(Float, default=0.0)
    summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(String(50), unique=True, index=True)
    case_id = Column(String(50), index=True)
    complainant_name = Column(String(150))
    incident_date = Column(DateTime, default=datetime.datetime.utcnow)
    portal_ref = Column(String(100))
    reported_loss = Column(Float)
    description = Column(Text)
    channel = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(50), unique=True, index=True)
    case_id = Column(String(50), index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    source_account = Column(String(100))
    destination_account = Column(String(100))
    amount = Column(Float)
    transaction_type = Column(String(50))
    location = Column(String(150))
    latitude = Column(Float)
    longitude = Column(Float)
    device_id = Column(String(100))
    ip_address = Column(String(100))
    channel = Column(String(50))
    beneficiary_bank = Column(String(100))
    risk_indicator = Column(String(20))
    layer_depth = Column(Integer, default=1)
    is_suspicious = Column(Boolean, default=False)

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(100), unique=True, index=True)
    account_holder = Column(String(150))
    bank_name = Column(String(100))
    branch = Column(String(100))
    account_type = Column(String(50))
    risk_score = Column(Float, default=50.0)
    total_incoming = Column(Float, default=0.0)
    total_outgoing = Column(Float, default=0.0)
    transaction_count = Column(Integer, default=0)
    is_flagged = Column(Boolean, default=False)
    kyc_status = Column(String(50), default="VERIFIED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(String(50), unique=True, index=True)
    name = Column(String(150), nullable=False)
    bank_name = Column(String(100))
    address = Column(String(250))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    risk_score = Column(Float, default=40.0)
    risk_level = Column(String(20), default="LOW")
    historical_withdrawals = Column(Integer, default=10)
    average_amount = Column(Float, default=25000.0)
    last_activity = Column(String(50), default="10 min ago")
    area = Column(String(100), default="Central")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(50), unique=True, index=True)
    predicted_location_id = Column(String(50))
    withdrawal_probability = Column(Float)
    risk_level = Column(String(20))
    predicted_time_window = Column(String(100))
    predicted_amount = Column(Float)
    distance_km = Column(Float)
    historical_similarity = Column(Float)
    top_factors = Column(Text)
    ranked_locations = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(50), unique=True, index=True)
    case_id = Column(String(50), index=True)
    location_id = Column(String(50))
    severity = Column(String(20), default="HIGH")
    probability = Column(Float, default=85.0)
    expected_time = Column(String(100))
    amount = Column(Float)
    status = Column(String(50), default="ACTIVE")
    recommended_action = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CaseAction(Base):
    __tablename__ = "case_actions"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(50), index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action_type = Column(String(100))
    description = Column(Text)
    officer_id = Column(String(50), default="demo_officer")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(200))
    full_name = Column(String(150))
    role = Column(String(50), default="Cyber Intelligence Officer")
    badge_number = Column(String(50), default="CYB-BLR-089")
''')

# 3. schemas.py
with open(os.path.join(base_dir, "schemas.py"), "w") as f:
    f.write('''import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    full_name: str
    role: str
    badge_number: str

class CaseBase(BaseModel):
    case_id: str
    fraud_type: str
    amount: float
    victim_name: str
    victim_phone: str
    victim_location: str
    status: str
    risk_level: str
    risk_score: float
    predicted_location_id: Optional[str] = None
    predicted_atm_name: Optional[str] = None
    predicted_time_window: Optional[str] = None
    predicted_amount: Optional[float] = None
    summary: Optional[str] = None

class CaseResponse(CaseBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class CaseStatusUpdate(BaseModel):
    status: str
    action_description: Optional[str] = None

class CaseActionResponse(BaseModel):
    id: int
    case_id: str
    timestamp: datetime.datetime
    action_type: str
    description: str
    officer_id: str

    class Config:
        from_attributes = True

class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    case_id: str
    timestamp: datetime.datetime
    source_account: str
    destination_account: str
    amount: float
    transaction_type: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    channel: Optional[str] = None
    beneficiary_bank: Optional[str] = None
    risk_indicator: str
    layer_depth: int
    is_suspicious: bool

    class Config:
        from_attributes = True

class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_holder: str
    bank_name: str
    branch: str
    account_type: str
    risk_score: float
    total_incoming: float
    total_outgoing: float
    transaction_count: int
    is_flagged: bool
    kyc_status: str

    class Config:
        from_attributes = True

class LocationResponse(BaseModel):
    id: int
    location_id: str
    name: str
    bank_name: str
    address: str
    latitude: float
    longitude: float
    risk_score: float
    risk_level: str
    historical_withdrawals: int
    average_amount: float
    last_activity: str
    area: str

    class Config:
        from_attributes = True

class FactorItem(BaseModel):
    name: str
    contribution: float
    impact: str

class RankedLocationItem(BaseModel):
    rank: int
    location_id: str
    name: str
    probability: float
    risk: str
    distance_km: float

class PredictionResponse(BaseModel):
    case_id: str
    predicted_location_id: str
    predicted_atm_name: str
    withdrawal_probability: float
    risk_level: str
    predicted_time_window: str
    predicted_amount: float
    distance_km: float
    historical_similarity: float
    top_factors: List[FactorItem]
    ranked_locations: List[RankedLocationItem]

class AlertCreate(BaseModel):
    case_id: str
    location_id: str
    severity: str = "HIGH"
    probability: float = 85.0
    expected_time: str = "23:30 – 00:30"
    amount: float = 185000.0
    recommended_action: str = "Dispatch field team and alert branch manager"

class AlertUpdate(BaseModel):
    status: str

class AlertResponse(BaseModel):
    id: int
    alert_id: str
    case_id: str
    location_id: str
    location_name: Optional[str] = None
    severity: str
    probability: float
    expected_time: str
    amount: float
    status: str
    recommended_action: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class ActionPayload(BaseModel):
    action_type: str
    description: str

class IngestionStats(BaseModel):
    records_received: int
    records_processed: int
    duplicates_removed: int
    suspicious_accounts: int
    suspicious_transactions: int
    last_ingestion_time: str
''')

print("Core files written successfully.")
