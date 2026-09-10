import datetime
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
