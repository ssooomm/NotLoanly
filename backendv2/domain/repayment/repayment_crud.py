from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, Categories, UserExpenses, RepaymentPlans
from domain.repayment.repayment_schema import *
from domain.common.common_crud import get_user

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
def save_repayment_plan(
        db: Session,
        plan: RepaymentPlanRequest
):
    try:
        # 사용자 확인
        user = get_user(db, plan.user_id)

        # 상환 기간 업데이트
        user.repayment_period = plan.repayment_period

        # 월별 상환 목표 계산 및 업데이트
        if user.loan_amount and plan.repayment_period:
            user.monthly_repayment_goal = user.loan_amount // plan.repayment_period
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid loan amount or repayment period"
            )

        # 해당 user_id의 모든 UserExpenses의 is_hard_to_reduce를 먼저 False로 설정
        db.query(UserExpenses) \
            .filter(UserExpenses.user_id == plan.user_id) \
            .update({UserExpenses.is_hard_to_reduce: False})

        # 지정된 category_ids에 대해 is_hard_to_reduce를 True로 설정
        db.query(UserExpenses) \
            .filter(
            UserExpenses.user_id == plan.user_id,
            UserExpenses.category_id.in_(plan.categories)
        ) \
            .update({UserExpenses.is_hard_to_reduce: True}, synchronize_session=False)

        db.commit()
        return "상환 계획이 저장되었습니다."

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
        plans = db.query(RepaymentPlans).filter_by(user_id=user_id).all()
        if not plans:
            return []

        return plans

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch repayment plans: {str(e)}"
        )


# 2-3-1. 상환 플랜 상세 조회
def get_repayment_plan(db: Session, plan_id: int, user_id: int) -> RepaymentPlans:
    try:
        plan = db.query(RepaymentPlans).filter_by(user_id=user_id, plan_id=plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Repayment plan not found"
            )
        return plan

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch repayment plan: {str(e)}"
        )


# 2-4. 상환 플랜 선택
def select_repayment_plan(db: Session, user_id: int, plan_id: int) -> str:
    try:
        # 사용자 확인
        user = get_user(db, user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        # 플랜 선택 업데이트
        user.selected_plan_group_id = plan_id
        db.commit()

        return "선택한 상환 플랜이 시작되었습니다."

    except HTTPException as http_ex:
        db.rollback()
        raise http_ex
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to select repayment plan: {str(e)}"
        )
