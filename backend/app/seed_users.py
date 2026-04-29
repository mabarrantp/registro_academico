from sqlalchemy.orm import Session
from app.models.user import User
from app.security import get_password_hash


def seed_users(db: Session):
    users = [
        ("admin", "admin123", "ADMIN", None),
        ("teacher1", "teacher123", "TEACHER", 1),  # teacher_id = 1
    ]

    created = 0
    for username, password, role, teacher_id in users:
        if db.query(User).filter(User.username == username).first():
            continue

        db.add(
            User(
                username=username,
                hashed_password=get_password_hash(password),
                role=role,
                teacher_id=teacher_id,
            )
        )
        created += 1

    db.commit()
    print(f"✅ Users sembrados ({created})")
