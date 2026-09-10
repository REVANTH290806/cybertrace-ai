import datetime
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
