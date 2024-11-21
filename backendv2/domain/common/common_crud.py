from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, Categories

def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_name(db: Session, user_id: int) -> str:
    """
    사용자 ID로 사용자 이름을 가져오는 함수
    """
    user = get_user(db, user_id)
    return user.name


def get_category_name(db: Session, category_id: int) -> str:
    """
    카테고리 ID로 카테고리 이름을 가져오는 함수
    """
    category = db.query(Categories).filter(Categories.category_id == category_id).first()
    if not category:
        return "Unknown"
    return category.category_name