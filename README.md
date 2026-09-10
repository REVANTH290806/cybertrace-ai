# CyberTrace AI

> **Predictive Cybercrime & Cash Withdrawal Intelligence Platform**  
> *Developed for Smart India Hackathon (SIH) — Problem Statement SIH26184*

---

## Important Prototype Disclaimer
> **"Prototype demonstration using synthetic/anonymized data. Predictions are decision-support outputs and are not definitive law-enforcement conclusions."**

---

## 1. Problem Statement (SIH26184)
> **"Development of a Predictive Analytics Framework for Cybercrime Complaints to Forecast Likely Cash Withdrawal Locations in Advance, Enabling Generation of Actionable Intelligence for Timely and Proactive Cybercrime Intervention."**

In digital financial fraud (UPI scams, phishing, fake investment schemes), stolen money is rapidly layered through multiple intermediary bank accounts ("mule networks") and physically withdrawn at ATM kiosks before victims realize they have been defrauded. Existing cybercrime response systems are purely reactive. 

**CyberTrace AI** flips this model from **reactive post-incident reporting** to **proactive real-time intercept intelligence**, predicting likely cash withdrawal ATM locations and time windows up to 2-4 hours before criminals can liquidate the cash.

---

## 2. Core Methodology & Workflow

```
Cybercrime Complaint (NCRP 1930)
        ↓
Data Ingestion (Banking Feeds, CBS, KYC, Threat Intel)
        ↓
Data Processing (Cleaning, Normalization, Duplicate Removal)
        ↓
Transaction Analysis (Multi-Hop Layering Graph: Victim → Mule → ATM)
        ↓
AI Risk Analysis (RandomForestClassifier, Gini/SHAP Explainability)
        ↓
Withdrawal Location Prediction (Ranked Candidate ATMs & Time Windows)
        ↓
Risk Map Visualization (Bengaluru Leaflet Map with Risk Heatmap)
        ↓
Real-Time Alert Dispatch (Threshold > 70% Dispatches Priority Alert)
        ↓
Law-Enforcement Action (Sec 102 CrPC Freeze, Patrol Intercept, CCTV Request)
        ↓
Case Monitoring / Resolution (Audit-Proof Intelligence Dossier)
```

---

## 3. Technology Stack

- **Frontend**:
  - React 19 + TypeScript + Vite
  - Tailwind CSS v4 (Clean, high-contrast law-enforcement styling)
  - React Router v7
  - Lucide React icons
  - Recharts (Analytical intelligence charts)
  - Leaflet + React-Leaflet + OpenStreetMap (Centred on Bengaluru)
- **Backend**:
  - Python 3.13
  - FastAPI (High-performance asynchronous REST API)
  - Pydantic v2 (Strict data validation)
  - SQLAlchemy ORM
- **Machine Learning & Data**:
  - `scikit-learn` (`RandomForestClassifier` with calibrated probability estimation)
  - `pandas` & `numpy` (Feature matrices, vector normalization)
- **Database**:
  - SQLite (Pre-configured and structured for smooth PostgreSQL/PostGIS migration)

---

## 4. Key Platform Modules

1. **Login Portal**: Secure credential access with pre-configured officer profile.
2. **Command Dashboard**: High-level operational KPIs, active cases queue, real-time alert feed, weekly cybercrime incident trend, and system health status.
3. **Case Investigation**: Deep-dive complainant information, loss breakdown, interactive status lifecycle stepper, action dispatch buttons (Alert Bank, Dispatch Field Team, Monitor ATM), and live timestamped audit timeline.
4. **Data Ingestion & Processing**: Multi-source ingestion (Complaints, Bank Feeds, KYC, Threat Feeds), processing pipeline counters, and raw telemetry inspection table.
5. **Transaction Intelligence**: Interactive visual money trail DAG (Victim → Layer 1 → Layer 2 → Layer 3 → Mule Account → Target ATM) with clickable node profiling.
6. **AI Risk Analysis & Prediction Result**: Showcase hero displaying **87.4% High Risk** for showcase case `CYB-1024`, predicted target **ATM A102 (Koramangala 80ft Rd)**, 23:30–00:30 window, explainability horizontal bar chart, and ranked alternative candidate ATMs.
7. **Predictive Risk Map**: Full-screen interactive Bengaluru city map showing ATM kiosks color-coded by risk (Red = High, Orange = Medium, Green = Low) with clickable intelligence cards.
8. **Real-Time Alerts**: Automated push console for high-risk cases, severity filters, acknowledgment actions, and a **"Simulate Incoming Alert"** dynamic test trigger.
9. **Analytics & Intelligence**: 8 comprehensive charts analyzing temporal liquidation vectors, hourly ATM rush hours, loss pool distributions, and risk trends.
10. **Investigation Reports**: Formal judicial and court-admissible Intelligence Dossier formatted for official export and one-click printing (`window.print()`).
11. **Settings**: Model hyperparameters, feature weights, and system health metrics.
12. **SIH Demo Mode Wizard**: Interactive 10-step guided tour walking evaluators through the exact showcase story from complaint receipt to ATM intercept.

---

## 5. Demo Credentials

| Role | Officer ID | Password |
| :--- | :--- | :--- |
| Cyber Intelligence Officer | `demo_officer` | `CyberTrace@123` |

---

## 6. Official SIH Showcase Case (`CYB-1024`)

- **Case ID**: `CYB-1024`
- **Fraud Type**: UPI Financial Fraud
- **Amount Defrauded**: ₹1,85,000
- **Complainant**: Rajesh Kumar (Koramangala, Bengaluru)
- **Primary Mule Account**: `ACC-MULE-204`
- **Forecasted Cash-Out ATM**: `ATM A102 - Koramangala 80ft Rd` (SBI Kiosk)
- **Withdrawal Probability**: **87.4%** (`HIGH RISK`)
- **Expected Time Window**: `23:30 – 00:30`
- **Distance from Last Hop**: `2.1 km`
- **Top Contributing Factors**:
  - Transaction Velocity: 82%
  - Historical Location Pattern: 76%
  - Time-of-Day Pattern: 68%
  - Mule Account Behavior: 61%
  - Location Risk Score: 53%

---

## 7. How to Run the Application

### Prerequisites
- Python 3.10+ (Python 3.13 recommended)
- Node.js 18+ and npm

### Step 1: Start Backend
```bash
cd backend
# Create virtual environment if not created
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI Server (starts on http://127.0.0.1:8000)
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 2: Start Frontend
```bash
cd frontend
# Install dependencies
npm install

# Run Vite Dev Server (starts on http://127.0.0.1:3000)
npm run dev -- --host 127.0.0.1 --port 3000
```

### Step 3: Access Application
Open your browser and navigate to:
```
http://127.0.0.1:3000
```
Log in using `demo_officer` and `CyberTrace@123`, or click **"Auto-fill Demo Credentials"**.

---

## 8. SIH Judge Presentation Flow (Step-by-Step)

1. **Login**: Authenticate as Officer `demo_officer`.
2. **Dashboard**: Highlight active case volume (124) and recent cases queue.
3. **Launch Demo**: Click the prominent **"START DEMO"** button in the top header.
4. **Step 1 - Cases**: Inspect Case `CYB-1024` (UPI Fraud, ₹1,85,000).
5. **Step 2 - Ingestion**: Review multi-source ingestion pipeline and processing statistics.
6. **Step 3 & 4 - Transactions**: Inspect interactive multi-hop graph leading to `ACC-MULE-204`.
7. **Step 5 & 6 - AI Prediction**: View **87.4% High Risk** forecast for `ATM A102` and explainability factor weights.
8. **Step 7 - Risk Map**: Locate `ATM A102` in Koramangala on the Leaflet Bengaluru map.
9. **Step 8 - Alerts**: Review priority alert `ALT-1024` and test **"Simulate Incoming Alert"**.
10. **Step 9 - Officer Action**: Trigger **"ALERT BANK"** and **"DISPATCH TEAM"**, observing live timeline updates.
11. **Step 10 - Report**: Export formal printable **Intelligence Dossier**.

---

## 9. Future Scope
- **Direct I4C & NPCI Switch Integration**: Real-time webhook listeners for instant transaction feeds.
- **Automated Sec 102 API Webhooks**: Automated direct debit freeze messages to nodal bank APIs.
- **Patrol Geofencing**: Integration with police PCR vans via mobile telemetry for automated nearest-patrol dispatch.
- **PostGIS Spatial Clustering**: Dynamic geo-density DBSCAN clustering over multi-city datasets.
