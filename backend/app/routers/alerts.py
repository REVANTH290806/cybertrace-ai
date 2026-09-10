import datetime
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
