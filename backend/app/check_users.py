from database import SessionLocal
from odels.user import User

db = SessionLocal()
print([(u.username, u.role, u.active) for u in db.query(User).all()])
db.close()