from database import SessionLocal
from models.quarter import Quarter


def run():
    db = SessionLocal()

    academic_year = 2025

    if db.query(Quarter).filter(Quarter.academic_year == academic_year).first():
        print(f"Quarters already seeded for {academic_year}")
        db.close()
        return

    quarters = [
        Quarter(code="QI", academic_year=academic_year, status="OPEN"),
        Quarter(code="QII", academic_year=academic_year, status="OPEN"),
        Quarter(code="QIII", academic_year=academic_year, status="OPEN"),
        Quarter(code="QIV", academic_year=academic_year, status="OPEN"),
    ]

    db.add_all(quarters)
    db.commit()
    db.close()

    print(f"✅ Quarters seeded for academic year {academic_year}")


if __name__ == "__main__":
    run()