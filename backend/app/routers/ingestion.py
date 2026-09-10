import datetime
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
