from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()
print([(u.username, u.role, u.active) for u in db.query(User).all()])
db.close()