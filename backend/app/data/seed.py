import datetime
import hashlib
import json
import random
from sqlalchemy.orm import Session
from ..models import Case, Complaint, Transaction, Account, Location, Prediction, Alert, CaseAction, User
from ..database import engine, Base

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# 22 Realistic Bengaluru ATM locations across key commercial & transit hubs
BENGALURU_LOCATIONS = [
    {"location_id": "ATM-A102", "name": "ATM A102 - Koramangala 80ft Rd", "bank_name": "State Bank of India", "address": "80 Feet Rd, 4th Block, Koramangala, Bengaluru", "lat": 12.9352, "lng": 77.6245, "risk_score": 88.5, "risk_level": "HIGH", "area": "Koramangala"},
    {"location_id": "ATM-A087", "name": "ATM A087 - Indiranagar 100ft Rd", "bank_name": "HDFC Bank", "address": "100 Feet Rd, HAL 2nd Stage, Indiranagar, Bengaluru", "lat": 12.9719, "lng": 77.6412, "risk_score": 78.2, "risk_level": "HIGH", "area": "Indiranagar"},
    {"location_id": "ATM-A104", "name": "ATM A104 - HSR Sector 1", "bank_name": "ICICI Bank", "address": "19th Main, Sector 1, HSR Layout, Bengaluru", "lat": 12.9121, "lng": 77.6446, "risk_score": 64.8, "risk_level": "MEDIUM", "area": "HSR Layout"},
    {"location_id": "ATM-A091", "name": "ATM A091 - MG Road Metro Kiosk", "bank_name": "Axis Bank", "address": "MG Road Metro Station Concourse, Bengaluru", "lat": 12.9754, "lng": 77.6066, "risk_score": 52.4, "risk_level": "MEDIUM", "area": "Central"},
    {"location_id": "ATM-A115", "name": "ATM A115 - Whitefield ITPL Main Rd", "bank_name": "Punjab National Bank", "address": "ITPL Main Rd, Kundalahalli, Whitefield, Bengaluru", "lat": 12.9856, "lng": 77.7289, "risk_score": 71.0, "risk_level": "HIGH", "area": "Whitefield"},
    {"location_id": "ATM-A042", "name": "ATM A042 - Electronic City Phase 1", "bank_name": "Canara Bank", "address": "Neeladri Rd, Phase 1, Electronic City, Bengaluru", "lat": 12.8399, "lng": 77.6770, "risk_score": 69.4, "risk_level": "MEDIUM", "area": "Electronic City"},
    {"location_id": "ATM-A073", "name": "ATM A073 - Jayanagar 4th Block", "bank_name": "Kotak Mahindra Bank", "address": "11th Main Rd, 4th Block, Jayanagar, Bengaluru", "lat": 12.9299, "lng": 77.5833, "risk_score": 38.0, "risk_level": "LOW", "area": "Jayanagar"},
    {"location_id": "ATM-A055", "name": "ATM A055 - Malleshwaram 8th Cross", "bank_name": "Bank of Baroda", "address": "Sampige Rd, 8th Cross, Malleshwaram, Bengaluru", "lat": 12.9988, "lng": 77.5711, "risk_score": 34.5, "risk_level": "LOW", "area": "Malleshwaram"},
    {"location_id": "ATM-A128", "name": "ATM A128 - BTM Layout 2nd Stage", "bank_name": "State Bank of India", "address": "7th Main, Outer Ring Rd, BTM 2nd Stage, Bengaluru", "lat": 12.9166, "lng": 77.6101, "risk_score": 75.8, "risk_level": "HIGH", "area": "BTM Layout"},
    {"location_id": "ATM-A063", "name": "ATM A063 - Marathahalli Bridge Kiosk", "bank_name": "Union Bank of India", "address": "Outer Ring Rd, Marathahalli Village, Bengaluru", "lat": 12.9569, "lng": 77.7011, "risk_score": 81.3, "risk_level": "HIGH", "area": "Marathahalli"},
    {"location_id": "ATM-A099", "name": "ATM A099 - Bellandur EcoSpace Junction", "bank_name": "HDFC Bank", "address": "Outer Ring Rd, Bellandur, Bengaluru", "lat": 12.9260, "lng": 77.6762, "risk_score": 63.2, "risk_level": "MEDIUM", "area": "Bellandur"},
    {"location_id": "ATM-A144", "name": "ATM A144 - Hebbal Flyover Circle", "bank_name": "ICICI Bank", "address": "Bellary Rd, Hebbal, Bengaluru", "lat": 13.0358, "lng": 77.5970, "risk_score": 58.7, "risk_level": "MEDIUM", "area": "Hebbal"},
    {"location_id": "ATM-A038", "name": "ATM A038 - Banashankari 2nd Stage", "bank_name": "Canara Bank", "address": "24th Cross, BSK 2nd Stage, Bengaluru", "lat": 12.9180, "lng": 77.5732, "risk_score": 32.1, "risk_level": "LOW", "area": "Banashankari"},
    {"location_id": "ATM-A160", "name": "ATM A160 - Rajajinagar 1st Block", "bank_name": "Axis Bank", "address": "Dr. Rajkumar Rd, Rajajinagar, Bengaluru", "lat": 12.9915, "lng": 77.5550, "risk_score": 44.0, "risk_level": "MEDIUM", "area": "Rajajinagar"},
    {"location_id": "ATM-A182", "name": "ATM A182 - Kalyan Nagar HRBR Layout", "bank_name": "State Bank of India", "address": "Kammanahalli Main Rd, HRBR Layout, Bengaluru", "lat": 13.0163, "lng": 77.6430, "risk_score": 66.5, "risk_level": "MEDIUM", "area": "Kalyan Nagar"},
    {"location_id": "ATM-A019", "name": "ATM A019 - Basavanagudi Gandhi Bazaar", "bank_name": "HDFC Bank", "address": "Gandhi Bazaar Main Rd, Basavanagudi, Bengaluru", "lat": 12.9438, "lng": 77.5738, "risk_score": 28.4, "risk_level": "LOW", "area": "Basavanagudi"},
    {"location_id": "ATM-A201", "name": "ATM A201 - Majestic KSRTC Bus Stand", "bank_name": "State Bank of India", "address": "Subhash Nagar, Majestic, Bengaluru", "lat": 12.9767, "lng": 77.5713, "risk_score": 86.9, "risk_level": "HIGH", "area": "Majestic"},
    {"location_id": "ATM-A215", "name": "ATM A215 - Yeshwanthpur Railway Kiosk", "bank_name": "Canara Bank", "address": "Tumkur Rd, Yeshwanthpur, Bengaluru", "lat": 13.0238, "lng": 77.5529, "risk_score": 79.1, "risk_level": "HIGH", "area": "Yeshwanthpur"},
    {"location_id": "ATM-A230", "name": "ATM A230 - Sarjapur Road Wipro Gate", "bank_name": "ICICI Bank", "address": "Sarjapur Main Rd, Kaikondrahalli, Bengaluru", "lat": 12.9103, "lng": 77.6834, "risk_score": 61.5, "risk_level": "MEDIUM", "area": "Sarjapur Rd"},
    {"location_id": "ATM-A244", "name": "ATM A244 - Yelahanka New Town 4th Phase", "bank_name": "Axis Bank", "address": "Major Sandeep Unnikrishnan Rd, Yelahanka, Bengaluru", "lat": 13.1007, "lng": 77.5963, "risk_score": 35.2, "risk_level": "LOW", "area": "Yelahanka"},
    {"location_id": "ATM-A260", "name": "ATM A260 - Kengeri Satellite Town", "bank_name": "Bank of Baroda", "address": "Kommaghatta Main Rd, Kengeri, Bengaluru", "lat": 12.9177, "lng": 77.4839, "risk_score": 41.0, "risk_level": "MEDIUM", "area": "Kengeri"},
    {"location_id": "ATM-A275", "name": "ATM A275 - RT Nagar Main Rd", "bank_name": "Union Bank of India", "address": "Dinnur Main Rd, RT Nagar, Bengaluru", "lat": 13.0189, "lng": 77.5960, "risk_score": 53.8, "risk_level": "MEDIUM", "area": "RT Nagar"}
]

FRAUD_TYPES = [
    "UPI Financial Fraud",
    "Investment Fraud",
    "Phishing Attack",
    "Online Shopping Fraud",
    "Identity Theft / Impersonation",
    "Banking SIM Swap",
    "Loan App Extortion"
]

def seed_database(db: Session):
    Base.metadata.create_all(bind=engine)
    if db.query(Case).count() >= 50 and db.query(Transaction).count() >= 500:
        print("Database already fully seeded.")
        return


    # 1. Seed Officer User
    existing_user = db.query(User).filter(User.username == "demo_officer").first()
    if not existing_user:
        user = User(
            username="demo_officer",
            hashed_password=hash_pw("CyberTrace@123"),
            full_name="Inspector Vikramaditya Rao",
            role="Cyber Intelligence Officer",
            badge_number="CYB-BLR-089"
        )
        db.add(user)

    # 2. Seed Locations
    for loc_data in BENGALURU_LOCATIONS:
        existing = db.query(Location).filter(Location.location_id == loc_data["location_id"]).first()
        if not existing:
            loc = Location(
                location_id=loc_data["location_id"],
                name=loc_data["name"],
                bank_name=loc_data["bank_name"],
                address=loc_data["address"],
                latitude=loc_data["lat"],
                longitude=loc_data["lng"],
                risk_score=loc_data["risk_score"],
                risk_level=loc_data["risk_level"],
                historical_withdrawals=random.randint(15, 85),
                average_amount=random.choice([20000.0, 35000.0, 50000.0, 100000.0]),
                last_activity=f"{random.randint(2, 45)} min ago",
                area=loc_data["area"]
            )
            db.add(loc)
    db.commit()

    # 3. Seed Accounts
    # Showcase Accounts
    accounts_data = [
        ("ACC-VICTIM-1024", "Rajesh Kumar (Victim)", "State Bank of India", "Koramangala Branch", "VICTIM", 10.0, 0.0, 185000.0, 1, False, "VERIFIED"),
        ("ACC-LAYER1-401", "Nexus Digital Solutions", "HDFC Bank", "Indiranagar Branch", "LAYER_1", 72.5, 185000.0, 185000.0, 4, True, "SUSPICIOUS"),
        ("ACC-LAYER2-712", "Apex Trading Corp", "ICICI Bank", "Whitefield Branch", "LAYER_2", 81.0, 185000.0, 120000.0, 6, True, "SUSPICIOUS"),
        ("ACC-LAYER3-889", "Star Pay Gateway Shell", "Axis Bank", "HSR Layout Branch", "LAYER_3", 89.2, 120000.0, 95000.0, 9, True, "FAKE_DOCS"),
        ("ACC-MULE-204", "Farooq Ahmed (Mule Operator)", "State Bank of India", "Koramangala Branch", "MULE_ACCOUNT", 96.4, 95000.0, 0.0, 14, True, "FAKE_DOCS")
    ]
    for acc in accounts_data:
        if not db.query(Account).filter(Account.account_number == acc[0]).first():
            db.add(Account(
                account_number=acc[0], account_holder=acc[1], bank_name=acc[2],
                branch=acc[3], account_type=acc[4], risk_score=acc[5],
                total_incoming=acc[6], total_outgoing=acc[7], transaction_count=acc[8],
                is_flagged=acc[9], kyc_status=acc[10]
            ))

    # Generate 50+ other synthetic accounts
    for i in range(1, 55):
        acc_num = f"ACC-SYN-{1000+i}"
        if not db.query(Account).filter(Account.account_number == acc_num).first():
            holder = f"Account Holder {1000+i}"
            b_name = random.choice(["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Canara Bank", "Bank of Baroda"])
            r_score = round(random.uniform(15.0, 95.0), 1)
            is_mule = r_score > 75.0
            acc_type = "MULE_ACCOUNT" if is_mule else random.choice(["VICTIM", "LAYER_1", "LAYER_2", "BENEFICIARY"])
            db.add(Account(
                account_number=acc_num,
                account_holder=holder,
                bank_name=b_name,
                branch=f"{random.choice(['Indiranagar', 'Koramangala', 'Whitefield', 'Jayanagar', 'HSR Layout'])} Branch",
                account_type=acc_type,
                risk_score=r_score,
                total_incoming=round(random.uniform(20000, 400000), 2),
                total_outgoing=round(random.uniform(15000, 380000), 2),
                transaction_count=random.randint(3, 25),
                is_flagged=is_mule,
                kyc_status="FAKE_DOCS" if is_mule else random.choice(["VERIFIED", "PARTIAL", "SUSPICIOUS"])
            ))
    db.commit()

    # 4. Showcase Case: CYB-1024
    if not db.query(Case).filter(Case.case_id == "CYB-1024").first():
        case_1024 = Case(
            case_id="CYB-1024",
            fraud_type="UPI Financial Fraud",
            amount=185000.0,
            victim_name="Rajesh Kumar",
            victim_phone="+91 98450 11928",
            victim_location="Koramangala, Bengaluru",
            status="HIGH-RISK PREDICTION",
            risk_level="HIGH",
            risk_score=87.4,
            predicted_location_id="ATM-A102",
            predicted_atm_name="ATM A102 - Koramangala 80ft Rd",
            predicted_time_window="23:30 – 00:30",
            predicted_amount=185000.0,
            summary="Victim defrauded through social engineering UPI collect request. Funds layered across 3 intermediary shell accounts within 14 minutes and channeled to dormant mule account ACC-MULE-204 with imminent cash liquidation predicted at Koramangala ATM A102.",
            created_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=48),
            updated_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=2)
        )
        db.add(case_1024)

        # Complaint
        db.add(Complaint(
            complaint_id="CMP-2026-1024",
            case_id="CYB-1024",
            complainant_name="Rajesh Kumar",
            incident_date=datetime.datetime.utcnow() - datetime.timedelta(hours=2),
            portal_ref="NCRP-2026-8921-KA",
            reported_loss=185000.0,
            description="Unauthorized UPI debit after receiving a spoofed utility bill payment link on WhatsApp.",
            channel="UPI"
        ))

        # Showcase Multi-hop Transactions
        t_base = datetime.datetime.utcnow() - datetime.timedelta(hours=1, minutes=40)
        showcase_txs = [
            ("TXN-1024-01", "ACC-VICTIM-1024", "ACC-LAYER1-401", 185000.0, "UPI", "Koramangala", 12.9350, 77.6240, "DEV-MOB-9901", "49.207.181.12", "Mobile Banking", "HDFC Bank", "HIGH", 1, True, t_base),
            ("TXN-1024-02", "ACC-LAYER1-401", "ACC-LAYER2-712", 185000.0, "IMPS", "Indiranagar", 12.9710, 77.6400, "DEV-DESK-4412", "103.211.54.89", "NetBanking", "ICICI Bank", "HIGH", 2, True, t_base + datetime.timedelta(minutes=4)),
            ("TXN-1024-03", "ACC-LAYER2-712", "ACC-LAYER3-889", 120000.0, "IMPS", "Whitefield", 12.9850, 77.7280, "DEV-MOB-8821", "117.202.99.14", "Immediate Payment", "Axis Bank", "HIGH", 3, True, t_base + datetime.timedelta(minutes=9)),
            ("TXN-1024-04", "ACC-LAYER3-889", "ACC-MULE-204", 95000.0, "IMPS", "HSR Layout", 12.9120, 77.6440, "DEV-MOB-7733", "14.139.155.22", "Immediate Payment", "State Bank of India", "HIGH", 4, True, t_base + datetime.timedelta(minutes=14)),
        ]
        for tx in showcase_txs:
            db.add(Transaction(
                transaction_id=tx[0], case_id="CYB-1024", timestamp=tx[15],
                source_account=tx[1], destination_account=tx[2], amount=tx[3],
                transaction_type=tx[4], location=tx[5], latitude=tx[6], longitude=tx[7],
                device_id=tx[8], ip_address=tx[9], channel=tx[10], beneficiary_bank=tx[11],
                risk_indicator=tx[12], layer_depth=tx[13], is_suspicious=tx[14]
            ))

        # Case Actions Timeline
        actions = [
            (t_base + datetime.timedelta(minutes=15), "Prediction Generated", "Predictive ML Engine forecasted 87.4% withdrawal probability at ATM A102."),
            (t_base + datetime.timedelta(minutes=16), "High-Risk Alert Created", "Automated priority alert dispatched to Central Operations Command."),
            (t_base + datetime.timedelta(minutes=18), "Bank Notification Initiated", "Formal Section 91 CrPC freeze directive issued to State Bank of India nodal officer."),
            (t_base + datetime.timedelta(minutes=20), "Field Team Dispatched", "Koramangala Sector Patrol Unit 4 notified for proactive ATM perimeter monitoring.")
        ]
        for act in actions:
            db.add(CaseAction(case_id="CYB-1024", timestamp=act[0], action_type=act[1], description=act[2], officer_id="demo_officer"))

        # Alert for CYB-1024
        db.add(Alert(
            alert_id="ALT-1024",
            case_id="CYB-1024",
            location_id="ATM-A102",
            severity="HIGH",
            probability=87.4,
            expected_time="23:30 – 00:30",
            amount=185000.0,
            status="ACTIVE",
            recommended_action="Deploy mobile intervention team to Koramangala 80ft Road ATM kiosk; alert SBI branch security desk.",
            created_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=25)
        ))

    # 5. Generate 55 Additional Realistic Cases and Transactions
    case_ids = [f"CYB-{1020 + i}" for i in range(1, 60) if f"CYB-{1020 + i}" != "CYB-1024"]
    for idx, cid in enumerate(case_ids):
        if not db.query(Case).filter(Case.case_id == cid).first():
            ftype = random.choice(FRAUD_TYPES)
            amt = round(random.uniform(15000.0, 450000.0), 2)
            loc = BENGALURU_LOCATIONS[idx % len(BENGALURU_LOCATIONS)]
            r_score = round(random.uniform(25.0, 92.0), 1)
            r_level = "HIGH" if r_score >= 70 else ("MEDIUM" if r_score >= 40 else "LOW")
            st = random.choice(["NEW", "UNDER ANALYSIS", "ALERT GENERATED", "ACTION INITIATED", "MONITORING", "RESOLVED"])
            
            new_case = Case(
                case_id=cid,
                fraud_type=ftype,
                amount=amt,
                victim_name=f"Complainant {cid}",
                victim_phone=f"+91 9{random.randint(1000, 9999)} {random.randint(10000, 99999)}",
                victim_location=f"{loc['area']}, Bengaluru",
                status=st,
                risk_level=r_level,
                risk_score=r_score,
                predicted_location_id=loc["location_id"],
                predicted_atm_name=loc["name"],
                predicted_time_window=f"{random.randint(18, 23)}:00 – {random.randint(0, 4):02d}:00",
                predicted_amount=round(amt * random.uniform(0.75, 0.98), 2),
                summary=f"Suspicious activity reported under {ftype}. Multi-hop account transaction trail detected with destination node mapped to {loc['name']}.",
                created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(2, 72)),
                updated_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(5, 120))
            )
            db.add(new_case)

            # Generate 4-8 transactions per case
            n_tx = random.randint(4, 9)
            curr_amt = amt
            src_acc = f"ACC-VICTIM-{cid}"
            t_event = datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(3, 48))

            for t_idx in range(n_tx):
                t_event += datetime.timedelta(minutes=random.randint(3, 18))
                dst_acc = f"ACC-SYN-{1001 + ((idx * 5 + t_idx) % 50)}"
                split_amt = round(curr_amt * random.uniform(0.65, 0.95), 2)
                db.add(Transaction(
                    transaction_id=f"TXN-{cid}-{t_idx+1}",
                    case_id=cid,
                    timestamp=t_event,
                    source_account=src_acc,
                    destination_account=dst_acc,
                    amount=split_amt,
                    transaction_type=random.choice(["IMPS", "NEFT", "UPI", "RTGS"]),
                    location=loc["area"],
                    latitude=loc["lat"] + random.uniform(-0.005, 0.005),
                    longitude=loc["lng"] + random.uniform(-0.005, 0.005),
                    device_id=f"DEV-{random.randint(1000, 9999)}",
                    ip_address=f"103.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
                    channel=random.choice(["UPI", "NetBanking", "Mobile Banking", "API Gateway"]),
                    beneficiary_bank=random.choice(["HDFC Bank", "ICICI Bank", "SBI", "Axis Bank"]),
                    risk_indicator="HIGH" if t_idx >= n_tx - 2 else "MEDIUM",
                    layer_depth=t_idx + 1,
                    is_suspicious=t_idx >= 1
                ))
                src_acc = dst_acc
                curr_amt = split_amt

            # Generate Case Timeline Action
            db.add(CaseAction(
                case_id=cid,
                timestamp=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
                action_type="Investigation Initialized",
                description=f"Automated ingestion parsed complaint and linked {n_tx} transaction trails.",
                officer_id="demo_officer"
            ))

            # Add Alert if High Risk
            if r_level == "HIGH" and random.random() > 0.3:
                db.add(Alert(
                    alert_id=f"ALT-{cid}",
                    case_id=cid,
                    location_id=loc["location_id"],
                    severity="HIGH",
                    probability=r_score,
                    expected_time=f"{random.randint(20, 23)}:00 – 01:00",
                    amount=amt,
                    status=random.choice(["ACTIVE", "ACKNOWLEDGED", "DISPATCHED"]),
                    recommended_action=f"High risk cash-out indicator at {loc['name']}. Alert branch surveillance.",
                    created_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(10, 240))
                ))
    
    db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    db = next(get_db())
    seed_database(db)
