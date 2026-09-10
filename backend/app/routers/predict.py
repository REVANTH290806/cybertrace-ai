from fastapi import APIRouter, Depends, HTTPException
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
