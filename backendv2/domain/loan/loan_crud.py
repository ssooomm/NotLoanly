from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, Categories, UserExpenses, RepaymentPlans
from domain.loan.loan_schema import *
from domain.common.common_crud import get_user

def apply_loan(
        db: Session,
        req: LoanApplicationRequest
):
    # 사용자 찾기
    user = get_user(db, req.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User not found."
        )

    try:
        # 사용자 대출 정보 업데이트
        user.loan_amount = req.loan_amount
        user.interest_rate = req.interest_rate
        db.commit()

        return "대출신청이 완료되었습니다."

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"대출 신청 중 오류 발생: {str(e)}"
        )
