import os

base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "app", "routers")

# 1. auth.py
with open(os.path.join(base_dir, "auth.py"), "w") as f:
    f.write('''import hashlib
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

@router.post("/login", response_model=UserResponse)
def login(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == creds.username).first()
    if not user or user.hashed_password != hash_pw(creds.password):
        if creds.username == "demo_officer" and creds.password == "CyberTrace@123":
            return UserResponse(
                username="demo_officer",
                full_name="Inspector Vikramaditya Rao",
                role="Cyber Intelligence Officer",
                badge_number="CYB-BLR-089"
            )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Officer ID or Password")
    return UserResponse(
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        badge_number=user.badge_number
    )
''')

# 2. cases.py
with open(os.path.join(base_dir, "cases.py"), "w") as f:
    f.write('''import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Case, CaseAction, Complaint
from ..schemas import CaseResponse, CaseStatusUpdate, CaseActionResponse, ActionPayload

router = APIRouter(prefix="/api/cases", tags=["cases"])

@router.get("", response_model=List[CaseResponse])
def get_cases(
    risk: Optional[str] = None,
    status: Optional[str] = None,
    fraud_type: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Case)
    if risk:
        query = query.filter(Case.risk_level == risk.upper())
    if status:
        query = query.filter(Case.status == status.upper())
    if fraud_type:
        query = query.filter(Case.fraud_type == fraud_type)
    if q:
        query = query.filter((Case.case_id.ilike(f"%{q}%")) | (Case.victim_name.ilike(f"%{q}%")) | (Case.predicted_atm_name.ilike(f"%{q}%")))
    return query.order_by(Case.id.asc()).all()

@router.get("/{case_id}")
def get_case_detail(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    complaint = db.query(Complaint).filter(Complaint.case_id == case_id).first()
    actions = db.query(CaseAction).filter(CaseAction.case_id == case_id).order_by(CaseAction.timestamp.asc()).all()
    
    return {
        "case": case,
        "complaint": complaint,
        "timeline": actions
    }

@router.put("/{case_id}/status")
def update_case_status(case_id: str, payload: CaseStatusUpdate, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    old_status = case.status
    case.status = payload.status
    case.updated_at = datetime.datetime.utcnow()
    
    action_desc = payload.action_description or f"Status transitioned from {old_status} to {payload.status}."
    action = CaseAction(
        case_id=case_id,
        timestamp=datetime.datetime.utcnow(),
        action_type="Status Transition",
        description=action_desc,
        officer_id="demo_officer"
    )
    db.add(action)
    db.commit()
    db.refresh(case)
    return {"status": "success", "case": case}

@router.post("/{case_id}/actions")
def add_case_action(case_id: str, payload: ActionPayload, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    action = CaseAction(
        case_id=case_id,
        timestamp=datetime.datetime.utcnow(),
        action_type=payload.action_type,
        description=payload.description,
        officer_id="demo_officer"
    )
    db.add(action)
    db.commit()
    return {"status": "success", "action": action}
''')

# 3. transactions.py
with open(os.path.join(base_dir, "transactions.py"), "w") as f:
    f.write('''from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Transaction, Account, Case, Location
from ..schemas import TransactionResponse, AccountResponse

router = APIRouter(prefix="/api", tags=["transactions"])

@router.get("/transactions/{case_id}", response_model=List[TransactionResponse])
def get_case_transactions(case_id: str, db: Session = Depends(get_db)):
    txs = db.query(Transaction).filter(Transaction.case_id == case_id).order_by(Transaction.timestamp.asc()).all()
    return txs

@router.get("/transactions/{case_id}/graph")
def get_transaction_graph(case_id: str, db: Session = Depends(get_db)):
    txs = db.query(Transaction).filter(Transaction.case_id == case_id).order_by(Transaction.timestamp.asc()).all()
    case = db.query(Case).filter(Case.case_id == case_id).first()
    
    if not txs:
        # Fallback graph for showcase
        return {"nodes": [], "edges": []}

    nodes = []
    edges = []
    seen_nodes = set()

    for idx, tx in enumerate(txs):
        # Source Node
        if tx.source_account not in seen_nodes:
            seen_nodes.add(tx.source_account)
            acc = db.query(Account).filter(Account.account_number == tx.source_account).first()
            node_type = "VICTIM" if idx == 0 else "SUSPICIOUS"
            nodes.append({
                "id": tx.source_account,
                "label": acc.account_holder if acc else tx.source_account,
                "type": node_type,
                "bank": acc.bank_name if acc else "Unknown Bank",
                "risk_score": acc.risk_score if acc else 50.0,
                "kyc": acc.kyc_status if acc else "UNVERIFIED"
            })

        # Destination Node
        if tx.destination_account not in seen_nodes:
            seen_nodes.add(tx.destination_account)
            acc = db.query(Account).filter(Account.account_number == tx.destination_account).first()
            is_last = (idx == len(txs) - 1)
            node_type = "MULE" if is_last else "INTERMEDIARY"
            nodes.append({
                "id": tx.destination_account,
                "label": acc.account_holder if acc else tx.destination_account,
                "type": node_type,
                "bank": acc.bank_name if acc else tx.beneficiary_bank or "Bank",
                "risk_score": acc.risk_score if acc else 85.0,
                "kyc": acc.kyc_status if acc else "FAKE_DOCS"
            })

        edges.append({
            "id": tx.transaction_id,
            "source": tx.source_account,
            "target": tx.destination_account,
            "amount": tx.amount,
            "channel": tx.channel or tx.transaction_type,
            "timestamp": tx.timestamp.strftime("%H:%M:%S"),
            "risk": tx.risk_indicator
        })

    # Add Target ATM Node linked to last mule account
    if case and case.predicted_location_id:
        atm_id = case.predicted_location_id
        if atm_id not in seen_nodes:
            seen_nodes.add(atm_id)
            nodes.append({
                "id": atm_id,
                "label": case.predicted_atm_name or "Target ATM Kiosk",
                "type": "ATM",
                "bank": "ATM Kiosk",
                "risk_score": case.risk_score,
                "kyc": "GEO_LOCATION"
            })
            if txs:
                last_mule = txs[-1].destination_account
                edges.append({
                    "id": f"PRED-{case.case_id}",
                    "source": last_mule,
                    "target": atm_id,
                    "amount": case.predicted_amount or case.amount,
                    "channel": "CASH_WITHDRAWAL_FORECAST",
                    "timestamp": case.predicted_time_window or "Expected",
                    "risk": "HIGH",
                    "is_predicted": True
                })

    return {"case_id": case_id, "nodes": nodes, "edges": edges}

@router.get("/accounts/{account_number}", response_model=AccountResponse)
def get_account_detail(account_number: str, db: Session = Depends(get_db)):
    acc = db.query(Account).filter(Account.account_number == account_number).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc
''')

# 4. predict.py
with open(os.path.join(base_dir, "predict.py"), "w") as f:
    f.write('''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Case, Transaction, Location
from ..schemas import PredictionResponse
from ..ml.engine import engine_instance

router = APIRouter(prefix="/api", tags=["prediction"])

@router.post("/predict/{case_id}", response_model=PredictionResponse)
@router.get("/predictions/{case_id}", response_model=PredictionResponse)
def predict_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    transactions = db.query(Transaction).filter(Transaction.case_id == case_id).all()
    locations = db.query(Location).order_by(Location.risk_score.desc()).all()
    
    prediction = engine_instance.predict_case(
        case_id=case.case_id,
        case_data={
            "amount": case.amount,
            "risk_score": case.risk_score,
            "fraud_type": case.fraud_type
        },
        transactions=transactions,
        available_locations=locations
    )
    return prediction

@router.get("/model/features")
def get_model_features():
    return {
        "model_type": "RandomForestClassifier",
        "framework": "scikit-learn",
        "trees": 100,
        "max_depth": 6,
        "status": "OPERATIONAL",
        "dataset": "Synthetic Prototype Liquidation Engine",
        "features": [
            {"feature": "transaction_amount", "description": "Total principal defraud value", "weight": 0.18},
            {"feature": "transaction_velocity", "description": "Hops per minute across payment gateways", "weight": 0.22},
            {"feature": "recent_tx_count", "description": "Rapid multi-hop burst count", "weight": 0.12},
            {"feature": "distance_from_prev_tx", "description": "Proximity to ATM physical location", "weight": 0.15},
            {"feature": "account_risk_score", "description": "Mule network classification score", "weight": 0.14},
            {"feature": "location_risk_score", "description": "Historical ATM terminal cash-out frequency", "weight": 0.11},
            {"feature": "suspicious_pattern_score", "description": "Immediate post-credit withdrawal heuristic", "weight": 0.08}
        ]
    }
''')

# 5. locations.py
with open(os.path.join(base_dir, "locations.py"), "w") as f:
    f.write('''from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Location, Case
from ..schemas import LocationResponse

router = APIRouter(prefix="/api/locations", tags=["locations"])

@router.get("", response_model=List[LocationResponse])
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).order_by(Location.risk_score.desc()).all()

@router.get("/{location_id}")
def get_location_detail(location_id: str, db: Session = Depends(get_db)):
    loc = db.query(Location).filter(Location.location_id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    
    nearby_cases = db.query(Case).filter(Case.predicted_location_id == location_id).all()
    return {
        "location": loc,
        "nearby_cases": nearby_cases,
        "active_cases_count": len(nearby_cases)
    }
''')

# 6. alerts.py
with open(os.path.join(base_dir, "alerts.py"), "w") as f:
    f.write('''import datetime
import random
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Alert, Case, Location, CaseAction
from ..schemas import AlertResponse, AlertCreate, AlertUpdate

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("", response_model=List[AlertResponse])
def get_alerts(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Alert)
    if status and status.upper() != "ALL":
        query = query.filter(Alert.status == status.upper())
    alerts = query.order_by(Alert.created_at.desc()).all()
    
    # attach location name
    result = []
    for a in alerts:
        loc = db.query(Location).filter(Location.location_id == a.location_id).first()
        res_dict = {
            "id": a.id,
            "alert_id": a.alert_id,
            "case_id": a.case_id,
            "location_id": a.location_id,
            "location_name": loc.name if loc else a.location_id,
            "severity": a.severity,
            "probability": a.probability,
            "expected_time": a.expected_time,
            "amount": a.amount,
            "status": a.status,
            "recommended_action": a.recommended_action,
            "created_at": a.created_at
        }
        result.append(AlertResponse(**res_dict))
    return result

@router.post("", response_model=AlertResponse)
def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    alert_num = random.randint(1000, 9999)
    alert_id = f"ALT-MAN-{alert_num}"
    
    new_alert = Alert(
        alert_id=alert_id,
        case_id=payload.case_id,
        location_id=payload.location_id,
        severity=payload.severity,
        probability=payload.probability,
        expected_time=payload.expected_time,
        amount=payload.amount,
        status="ACTIVE",
        recommended_action=payload.recommended_action
    )
    db.add(new_alert)

    # Log action to case timeline
    action = CaseAction(
        case_id=payload.case_id,
        timestamp=datetime.datetime.utcnow(),
        action_type="Alert Generated",
        description=f"Manual high-priority alert {alert_id} dispatched for location {payload.location_id}.",
        officer_id="demo_officer"
    )
    db.add(action)

    db.commit()
    db.refresh(new_alert)

    loc = db.query(Location).filter(Location.location_id == new_alert.location_id).first()
    return AlertResponse(
        id=new_alert.id,
        alert_id=new_alert.alert_id,
        case_id=new_alert.case_id,
        location_id=new_alert.location_id,
        location_name=loc.name if loc else new_alert.location_id,
        severity=new_alert.severity,
        probability=new_alert.probability,
        expected_time=new_alert.expected_time,
        amount=new_alert.amount,
        status=new_alert.status,
        recommended_action=new_alert.recommended_action,
        created_at=new_alert.created_at
    )

@router.put("/{alert_id}")
def update_alert(alert_id: str, payload: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = payload.status
    
    # Log timeline action
    action = CaseAction(
        case_id=alert.case_id,
        timestamp=datetime.datetime.utcnow(),
        action_type=f"Alert Status: {payload.status}",
        description=f"Officer updated Alert {alert_id} status to {payload.status}.",
        officer_id="demo_officer"
    )
    db.add(action)
    db.commit()
    return {"status": "success", "alert_id": alert_id, "new_status": payload.status}

@router.post("/simulate")
def simulate_incoming_alert(db: Session = Depends(get_db)):
    locs = db.query(Location).filter(Location.risk_score > 70).all()
    cases = db.query(Case).filter(Case.status != "RESOLVED").all()
    
    loc = random.choice(locs) if locs else None
    case = random.choice(cases) if cases else None

    c_id = case.case_id if case else "CYB-1024"
    loc_id = loc.location_id if loc else "ATM-A102"
    prob = round(random.uniform(76.0, 94.5), 1)
    amt = round(random.uniform(50000.0, 250000.0), 2)
    alt_id = f"ALT-SIM-{random.randint(2000, 9999)}"

    new_alert = Alert(
        alert_id=alt_id,
        case_id=c_id,
        location_id=loc_id,
        severity="HIGH",
        probability=prob,
        expected_time=f"{random.randint(21, 23)}:30 – 01:00",
        amount=amt,
        status="ACTIVE",
        recommended_action=f"Immediate surveillance recommended at {loc.name if loc else loc_id}. Rapid cash drainage suspected.",
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return {
        "message": "Real-time alert simulated successfully",
        "alert": {
            "alert_id": new_alert.alert_id,
            "case_id": new_alert.case_id,
            "location_id": new_alert.location_id,
            "location_name": loc.name if loc else loc_id,
            "probability": new_alert.probability,
            "amount": new_alert.amount,
            "expected_time": new_alert.expected_time,
            "severity": new_alert.severity,
            "status": new_alert.status
        }
    }
''')

# 7. analytics.py
with open(os.path.join(base_dir, "analytics.py"), "w") as f:
    f.write('''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Case, Location, Alert

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("")
def get_analytics(db: Session = Depends(get_db)):
    total_cases = db.query(Case).count()
    high_risk_cases = db.query(Case).filter(Case.risk_level == "HIGH").count()
    med_risk_cases = db.query(Case).filter(Case.risk_level == "MEDIUM").count()
    low_risk_cases = db.query(Case).filter(Case.risk_level == "LOW").count()
    
    total_amount = db.query(func.sum(Case.amount)).scalar() or 38600000.0
    active_alerts = db.query(Alert).filter(Alert.status == "ACTIVE").count()

    # Fraud types distribution
    fraud_counts = db.query(Case.fraud_type, func.count(Case.id)).group_by(Case.fraud_type).all()
    fraud_distribution = [{"type": f[0], "count": f[1]} for f in fraud_counts]

    # Withdrawals by hour (synthetic distribution matching peak night patterns)
    hourly_withdrawals = [
        {"hour": "00:00", "count": 28, "risk": "HIGH"},
        {"hour": "02:00", "count": 34, "risk": "HIGH"},
        {"hour": "04:00", "count": 18, "risk": "MEDIUM"},
        {"hour": "06:00", "count": 7, "risk": "LOW"},
        {"hour": "08:00", "count": 9, "risk": "LOW"},
        {"hour": "10:00", "count": 14, "risk": "LOW"},
        {"hour": "12:00", "count": 19, "risk": "LOW"},
        {"hour": "14:00", "count": 22, "risk": "MEDIUM"},
        {"hour": "16:00", "count": 26, "risk": "MEDIUM"},
        {"hour": "18:00", "count": 31, "risk": "MEDIUM"},
        {"hour": "20:00", "count": 38, "risk": "HIGH"},
        {"hour": "22:00", "count": 45, "risk": "HIGH"}
    ]

    # Cases over time (weekly trend)
    timeline_trend = [
        {"period": "Week 1", "cases": 18, "amount": 4200000, "prevented": 1400000},
        {"period": "Week 2", "cases": 24, "amount": 6100000, "prevented": 2800000},
        {"period": "Week 3", "cases": 31, "amount": 7900000, "prevented": 3900000},
        {"period": "Week 4", "cases": 28, "amount": 8400000, "prevented": 4200000},
        {"period": "Week 5", "cases": 35, "amount": 10200000, "prevented": 5800000},
        {"period": "Current", "cases": 42, "amount": 12800000, "prevented": 7100000}
    ]

    # Top high-risk ATM locations
    top_locs = db.query(Location).order_by(Location.risk_score.desc()).limit(6).all()
    high_risk_locations = [
        {"location": l.name.split(" - ")[1] if " - " in l.name else l.name, "score": l.risk_score, "withdrawals": l.historical_withdrawals}
        for l in top_locs
    ]

    return {
        "summary": {
            "total_cases": total_cases,
            "total_amount_inr": total_amount,
            "high_risk_cases": high_risk_cases,
            "medium_risk_cases": med_risk_cases,
            "low_risk_cases": low_risk_cases,
            "active_alerts": active_alerts,
            "avg_confidence": 84.6
        },
        "risk_distribution": [
            {"name": "High Risk", "value": high_risk_cases, "color": "#ef4444"},
            {"name": "Medium Risk", "value": med_risk_cases, "color": "#f59e0b"},
            {"name": "Low Risk", "value": low_risk_cases, "color": "#10b981"}
        ],
        "fraud_distribution": fraud_distribution,
        "hourly_withdrawals": hourly_withdrawals,
        "timeline_trend": timeline_trend,
        "high_risk_locations": high_risk_locations
    }
''')

# 8. ingestion.py
with open(os.path.join(base_dir, "ingestion.py"), "w") as f:
    f.write('''import datetime
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Case, Transaction, Account
from ..data.seed import seed_database
from ..schemas import IngestionStats

router = APIRouter(prefix="/api/ingest", tags=["ingestion"])

@router.get("/stats", response_model=IngestionStats)
def get_ingestion_stats(db: Session = Depends(get_db)):
    tx_count = db.query(Transaction).count()
    acc_count = db.query(Account).count()
    mule_count = db.query(Account).filter(Account.account_type == "MULE_ACCOUNT").count()
    suspicious_tx = db.query(Transaction).filter(Transaction.is_suspicious == True).count()
    
    return IngestionStats(
        records_received=tx_count + 120,
        records_processed=tx_count,
        duplicates_removed=14,
        suspicious_accounts=mule_count,
        suspicious_transactions=suspicious_tx,
        last_ingestion_time="Just now"
    )

@router.post("/process")
def process_data(db: Session = Depends(get_db)):
    # Simulates execution of data cleaning, normalization, duplicate detection, graph synthesis
    tx_count = db.query(Transaction).count()
    return {
        "status": "success",
        "stage": "MODEL_READY",
        "records_received": tx_count + 120,
        "records_cleaned": tx_count,
        "duplicates_removed": 14,
        "accounts_linked": 58,
        "features_engineered": [
            "transaction_velocity",
            "hop_latency_minutes",
            "distance_decay_factor",
            "mule_network_eigenvector",
            "temporal_anomaly_score"
        ]
    }

@router.post("/reset-demo")
def reset_demo_dataset(db: Session = Depends(get_db)):
    seed_database(db)
    return {"status": "success", "message": "Demo dataset re-initialized successfully."}
''')

# 9. reports.py
with open(os.path.join(base_dir, "reports.py"), "w") as f:
    f.write('''import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Case, Complaint, Transaction, Location, CaseAction, Alert

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.post("/{case_id}")
def generate_case_report(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    complaint = db.query(Complaint).filter(Complaint.case_id == case_id).first()
    txs = db.query(Transaction).filter(Transaction.case_id == case_id).order_by(Transaction.timestamp.asc()).all()
    actions = db.query(CaseAction).filter(CaseAction.case_id == case_id).order_by(CaseAction.timestamp.asc()).all()
    alert = db.query(Alert).filter(Alert.case_id == case_id).order_by(Alert.created_at.desc()).first()
    loc = db.query(Location).filter(Location.location_id == case.predicted_location_id).first()

    report_dossier = {
        "report_id": f"INTEL-REP-{case.case_id}-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M')}",
        "generated_at": datetime.datetime.utcnow().strftime("%d-%b-%Y %H:%M:%S UTC"),
        "classification": "CONFIDENTIAL // LAW ENFORCEMENT DECISION SUPPORT ONLY",
        "investigating_unit": "Cybercrime Investigation Division, CID Karnataka",
        "case_id": case.case_id,
        "fraud_type": case.fraud_type,
        "defrauded_amount": case.amount,
        "victim_profile": {
            "name": case.victim_name,
            "contact": case.victim_phone,
            "residence": case.victim_location,
            "ncrp_portal_ref": complaint.portal_ref if complaint else "NCRP-2026-PENDING",
            "incident_date": complaint.incident_date.strftime("%d-%b-%Y %H:%M") if complaint else "Reported Today"
        },
        "forecasting_summary": {
            "predicted_atm": case.predicted_atm_name or (loc.name if loc else "Target ATM"),
            "location_address": loc.address if loc else "Koramangala, Bengaluru",
            "withdrawal_probability": f"{case.risk_score}%",
            "risk_tier": case.risk_level,
            "expected_time_window": case.predicted_time_window or "23:30 – 00:30",
            "estimated_cash_out": case.predicted_amount or case.amount
        },
        "contributing_factors": [
            {"factor": "High Transaction Velocity", "weight": "82%", "observation": "4 hops executed within 14 minutes"},
            {"factor": "Historical Location Pattern", "weight": "76%", "observation": "Syndicate recurringly cashes out in Koramangala hub"},
            {"factor": "Time-of-day pattern", "weight": "68%", "observation": "Night-time liquidation window scheduled"},
            {"factor": "Mule Account KYC Deficiency", "weight": "61%", "observation": "Recently dormant account reactivated with high volume"}
        ],
        "transaction_trail": [
            {
                "txn_id": t.transaction_id,
                "timestamp": t.timestamp.strftime("%d-%b %H:%M:%S"),
                "from_account": t.source_account,
                "to_account": t.destination_account,
                "amount": t.amount,
                "channel": t.channel or t.transaction_type,
                "bank": t.beneficiary_bank
            }
            for t in txs
        ],
        "timeline_events": [
            {
                "time": a.timestamp.strftime("%H:%M:%S"),
                "action": a.action_type,
                "details": a.description,
                "officer": a.officer_id
            }
            for a in actions
        ],
        "recommended_directives": [
            "Issue immediate account debit freeze under Sec 102 CrPC to beneficiary banks.",
            "Dispatch mobile intercept team to designated ATM terminal perimeter.",
            "Request preservation of CCTV footage from bank branch surveillance officer.",
            "Flag destination mule accounts across National Cybercrime Threat Analytics (NCTAU)."
        ],
        "disclaimer": "PROTOTYPE DEMONSTRATION USING SYNTHETIC/ANONYMIZED DATA. PREDICTIONS ARE DECISION-SUPPORT OUTPUTS AND ARE NOT DEFINITIVE LAW-ENFORCEMENT CONCLUSIONS."
    }

    return report_dossier
''')

print("All routers created successfully.")
