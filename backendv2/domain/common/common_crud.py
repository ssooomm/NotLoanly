from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User

def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user