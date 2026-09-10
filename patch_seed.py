import re

seed_path = "/Users/revanth/.gemini/antigravity/scratch/cybertrace-ai/backend/app/data/seed.py"
with open(seed_path, "r") as f:
    content = f.read()

# Add fast path at the beginning of seed_database
replacement = """def seed_database(db: Session):
    Base.metadata.create_all(bind=engine)
    if db.query(Case).count() >= 50 and db.query(Transaction).count() >= 500:
        print("Database already fully seeded.")
        return
"""

content = re.sub(r"def seed_database\(db: Session\):\s+Base\.metadata\.create_all\(bind=engine\)", replacement, content)
with open(seed_path, "w") as f:
    f.write(content)
print("Patched seed.py successfully")
