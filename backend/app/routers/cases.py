import datetime
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
