from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Tuple, Dict, Any, List
from models import User, Categories, UserExpenses, RepaymentPlans
from domain.repayment.repayment_schema import *

import json

def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
def save_repayment_plan(
        db: Session,
        user_id: int,
        category_ids: List[int],
        repayment_period: int
) -> dict:
    try:
        # 사용자 확인
        user = get_user(db, user_id)

        # 상환 기간 업데이트
        user.repayment_period = repayment_period

        # 월별 상환 목표 계산 및 업데이트
        if user.loan_amount and repayment_period:
            user.monthly_repayment_goal = user.loan_amount // repayment_period
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid loan amount or repayment period"
            )

        # 기존 UserExpenses 레코드들의 is_hard_to_reduce를 모두 False로 설정
        db.query(UserExpenses) \
            .filter(UserExpenses.user_id == user_id) \
            .update({UserExpenses.is_hard_to_reduce: False})

        # 선택된 카테고리들의 is_hard_to_reduce를 True로 설정
        for category_id in category_ids:
            user_expense = db.query(UserExpenses).filter(
                UserExpenses.user_id == user_id,
                UserExpenses.category_id == category_id
            ).first()

            if user_expense:
                user_expense.is_hard_to_reduce = True
            else:
                new_expense = UserExpenses(
                    user_id=user_id,
                    category_id=category_id,
                    month=11,  # 기본값
                    original_amount=0,  # 초기값
                    is_hard_to_reduce=True
                )
                db.add(new_expense)

        db.commit()
        return {
            "status": "success",
            "message": "상환 계획이 저장되었습니다."
        }

    except HTTPException as http_ex:
        db.rollback()
        raise http_ex

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# 2-3. 상환 플랜 리스트 조회
def get_repayment_plans(db: Session, user_id: int) -> RepaymentPlans:
    try:
        # Query repayment plans for the user
        plans = db.query(RepaymentPlans).filter_by(user_id=user_id).all()
        if not plans:
            return []
            
        return plans

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch repayment plans: {str(e)}"
        )
