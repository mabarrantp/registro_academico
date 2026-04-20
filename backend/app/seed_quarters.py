from app.database import SessionLocal
from app.models.quarter import Quarter

db = SessionLocal()

quarters = [
    Quarter(code="QI", academic_year=2025, status="OPEN"),
    Quarter(code="QII", academic_year=2025, status="OPEN"),
    Quarter(code="QIII", academic_year=2025, status="OPEN"),
    Quarter(code="QIV", academic_year=2025, status="OPEN"),
]

for q in quarters:
    exists = (
        db.query(Quarter)
        .filter(Quarter.code == q.code, Quarter.academic_year == q.academic_year)
        .first()
    )
    if not exists:
        db.add(q)

db.commit()
db.close()

print("✅ Quarters seeded")