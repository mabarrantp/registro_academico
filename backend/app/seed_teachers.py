from sqlalchemy.orm import Session
from app.models.teacher import Teacher


def run(db: Session):
    teachers = [
        ("Fatima", "Lara"),
        ("Ana", "Palacio"),
        ("Francis", "Herrera"),
        ("Yorleni", "Vilchez"),
        ("Wendy", "Alonso"),
        ("Richard", "Valenzuela"),
        ("Sharon", "Jonga"),
        ("Ena", "Mora"),
        ("Rosa", "Gomez"),
        ("Freddy", "Vilchez"),
        ("Honorio", "Navarrete"),
        ("Dulce", "Castellon"),
        ("Edgardo", "Sirias"),
        ("Marcos", "Barrantes"),
        ("Francisco", "Meneses"),
        ("Oswaldo", "Rivas"),
        ("Selena", "Castillo"),
        ("Keren", "Lanzas"),
        ("Libny", "Hernandez"),
        ("Gabriela", "Zamora"),
        ("Nathali", "Muller"),
        ("Jairo", "Flores"),
    ]

    created = 0
    for first, last in teachers:
        exists = (
            db.query(Teacher)
            .filter(
                Teacher.first_name == first,
                Teacher.last_name == last,
            )
            .first()
        )
        if not exists:
            db.add(Teacher(first_name=first, last_name=last, active=True))
            created += 1

    db.commit()
    print(f"✅ Teachers sembrados ({created})")
