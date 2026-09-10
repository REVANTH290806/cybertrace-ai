from typing import List
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
