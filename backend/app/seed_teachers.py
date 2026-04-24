from database import SessionLocal
from models.teacher import Teacher


def run():
    db = SessionLocal()

    teachers = [
        Teacher(first_name="Fatima", last_name="Lara"),
        Teacher(first_name="Ana", last_name="Palacio"),
        Teacher(first_name="Francis", last_name="Herrera"),
        Teacher(first_name="Yorleni", last_name="Vilchez"),
        Teacher(first_name="Wendy", last_name="Alonso"),
        Teacher(first_name="Richard", last_name="Valenzuela"),
        Teacher(first_name="Sharon", last_name="Jonga"),
        Teacher(first_name="Ena", last_name="Mora"),
        Teacher(first_name="Rosa", last_name="Gomez"),
        Teacher(first_name="Freddy", last_name="Vilchez"),
        Teacher(first_name="Honorio", last_name="Navarrete"),
        Teacher(first_name="Dulce", last_name="Castellon"),
        Teacher(first_name="Edgardo", last_name="Sirias"),
        Teacher(first_name="Marcos", last_name="Barrantes"),
        Teacher(first_name="Francisco", last_name="Meneses"),
        Teacher(first_name="Oswaldo", last_name="Rivas"),
        Teacher(first_name="Selena", last_name="Castillo"),
        Teacher(first_name="Keren", last_name="Lanzas"),
        Teacher(first_name="Libny", last_name="Hernandez"),
        Teacher(first_name="Gabriela", last_name="Zamora"),
        Teacher(first_name="Nathali", last_name="Muller"),
        Teacher(first_name="Jairo", last_name="Flores"),
    ]

    created = 0
    skipped = 0

    for t in teachers:
        exists = (
            db.query(Teacher)
            .filter(
                Teacher.first_name == t.first_name,
                Teacher.last_name == t.last_name,
            )
            .first()
        )

        if exists:
            skipped += 1
        else:
            db.add(t)
            created += 1

    db.commit()
    db.close()

    print(f"✅ Teachers cargados | created={created} skipped={skipped}")


if __name__ == "__main__":
    run()