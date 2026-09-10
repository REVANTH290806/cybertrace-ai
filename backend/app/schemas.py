import datetime
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
