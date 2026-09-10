# CyberTrace AI: System Architecture & Technical Methodology

## Problem Statement SIH26184
"Development of a Predictive Analytics Framework for Cybercrime Complaints to Forecast Likely Cash Withdrawal Locations in Advance, Enabling Generation of Actionable Intelligence for Timely and Proactive Cybercrime Intervention."

---

## 1. End-to-End Pipeline Architecture

```
DATA SOURCES (NCRP 1930, Bank Switches, KYC Registries, Threat Intel)
    ↓
DATA INGESTION (FastAPI Batch & Webhook Streams)
    ↓
DATA PROCESSING (Cleaning, Normalization, Duplicate Removal)
    ↓
FEATURE ENGINEERING (Velocity, Hop Latency, Distance Decay, Account Risk)
    ↓
TRANSACTION GRAPH (Directed Multi-Hop Fund Flow: Victim → Mule → ATM)
    ↓
AI RISK ANALYSIS (RandomForestClassifier, Gini/SHAP Explainability)
    ↓
LOCATION & TIME PREDICTION (Candidate ATM Terminals & 2-Hour Off-Peak Windows)
    ↓
GIS VISUALIZATION (Bengaluru Leaflet Map with Risk Heatmap & Popups)
    ↓
REAL-TIME ALERT (Automated Priority Dispatch for Threshold > 70%)
    ↓
LAW ENFORCEMENT ACTION (Sec 102 Debit Freeze, Field Intercept, CCTV Preservation)
    ↓
CASE MONITORING & RESOLUTION (Audit-Ready Forensic Dossier & Timeline)
```

---

## 2. Machine Learning Approach

### Core Features:
1. **Transaction Velocity**: Number of inter-bank hops completed per hour.
2. **Transaction Amount**: Normalized principal value compared against ATM daily limits.
3. **Hop Latency**: Time difference between intermediary account transfers.
4. **Physical Distance**: Distance between recent mobile IP/device login and target ATM terminal.
5. **Temporal Profile**: Time-of-day risk factor (night-time / off-peak window analysis).
6. **Mule Account Risk**: KYC deficiency, account age, and historical flag status.
7. **ATM Terminal Risk**: Historical frequency of fraudulent cash-outs at kiosk.
8. **Cash Drain Pattern**: Ratio of incoming funds transferred or withdrawn within 30 minutes.

### Algorithmic Engine:
- `RandomForestClassifier` (100 estimators, max depth 6) implemented via `scikit-learn`.
- Output: Calibrated liquidation probability ($0.0 - 100.0\%$), classified into Low ($<40\%$), Medium ($40-69\%$), and High ($\ge 70\%$).
- Explainability: Horizontal contribution weights highlighting the primary behavioral factors driving the forecast.

---

## 3. Database Schema (SQLite & PostGIS-Ready)
- `cases`: Comprehensive case status, reported loss, complainant details, predicted ATM, and risk level.
- `complaints`: NCRP portal reference, channel, reported description, and timestamp.
- `transactions`: Multi-hop financial records with layer depth, channel, IP, device, and suspicious flag.
- `accounts`: Account profiling, risk score, KYC status, and cumulative incoming/outgoing volumes.
- `locations`: ATM terminal registry with coordinates, historical liquidation count, bank, and jurisdiction.
- `predictions`: Stored inference snapshots with top feature weights and ranked alternative ATMs.
- `alerts`: Actionable real-time alerts with severity, probability, status, and recommended protocols.
- `case_actions`: Immutable audit log tracking officer interventions and status transitions.
- `users`: Law-enforcement officer profiles with role-based access.

---

## 4. Legal & Synthetic Data Disclaimer
All prototype predictions use synthetic/anonymized demonstration data and are intended for decision support only. Predictions are decision-support outputs and are not definitive law-enforcement conclusions.
