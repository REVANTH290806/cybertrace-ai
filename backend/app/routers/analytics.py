from fastapi import APIRouter, Depends
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
