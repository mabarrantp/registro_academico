from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password

db = SessionLocal()

users = [
    ("teacher1", "1234", "TEACHER"),
    ("coord1", "1234", "COORDINATION"),
    ("admin1", "1234", "ADMIN"),
]

for username, password, role in users:
    exists = db.query(User).filter(User.username == username).first()
    if not exists:
        db.add(
            User(
                username=username,
                hashed_password=hash_password(password),
                role=role,
                active=True
            )
        )

db.commit()
db.close()

print("✅ Users seeded")