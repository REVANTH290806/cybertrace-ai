from typing import List
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
