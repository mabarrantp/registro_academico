from database import SessionLocal
from models.user import User
from security import hash_password

def run():
    db = SessionLocal()

    if db.query(User).first():
        print("Users already seeded")
        db.close()
        return

    users = [
        User(username="admin", hashed_password=hash_password("admin123"), role="ADMIN", active=True),
        User(username="teacher", hashed_password=hash_password("teacher123"), role="TEACHER", active=True),
    ]

    db.add_all(users)
    db.commit()
    db.close()

    print("✅ Users seeded")

if __name__ == "__main__":
    run()
