import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .data.seed import seed_database
from .routers import auth, cases, transactions, predict, locations, alerts, analytics, ingestion, reports

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB & Seed data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title="CyberTrace AI",
    description="Predictive Cybercrime & Cash Withdrawal Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(transactions.router)
app.include_router(predict.router)
app.include_router(locations.router)
app.include_router(alerts.router)
app.include_router(analytics.router)
app.include_router(ingestion.router)
app.include_router(reports.router)

@app.get("/api/health")
def get_health():
    return {
        "status": "healthy",
        "system": "CyberTrace AI Predictive Engine",
        "version": "1.0.0-PROTOTYPE",
        "services": {
            "data_ingestion": "online",
            "ai_engine": "online",
            "database": "online",
            "alert_service": "online"
        },
        "mode": "Demonstration Prototype (Synthetic/Anonymized Data)"
    }

@app.get("/api/disclaimer")
def get_disclaimer():
    return {
        "disclaimer": "Prototype demonstration using synthetic/anonymized data. Predictions are decision-support outputs and are not definitive law-enforcement conclusions."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
