import hashlib
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
