from sqlalchemy.orm import Session

from app.models.quarter import Quarter


def seed_quarters(db: Session, academic_year: int = 2025):
    quarters = [
        ("Q1", academic_year),
        ("Q2", academic_year),
        ("Q3", academic_year),
        ("Q4", academic_year),
    ]

    created = 0
    skipped = 0

    for code, year in quarters:
        exists = (
            db.query(Quarter)
            .filter(
                Quarter.code == code,
                Quarter.academic_year == year,
            )
            .first()
        )

        if exists:
            skipped += 1
            continue

        db.add(
            Quarter(
                code=code,
                academic_year=year,
                status="OPEN",
            )
        )
        created += 1

    db.commit()

    print(
        f"✅ Quarters sembrados | created={created} skipped={skipped}"
    )