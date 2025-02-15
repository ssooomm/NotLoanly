from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.repayment import repayment_schema, repayment_crud, gpt_service
from domain.common.common_schema import PostResponse

router = APIRouter(
    prefix="/api/repayment",
)


# 2-1. - 사용 보류

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
@router.post("/save-plan", response_model=PostResponse)
async def save_plan(
        plan: repayment_schema.RepaymentPlanRequest,
        db: Session = Depends(get_db)
):
    try:
        message = repayment_crud.save_repayment_plan(
            db, plan
        )
        return {
            "status": "success",
            "message": message
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

#2-2-1 gpt
@router.post("/analyze-and-insert-plans")
def analyze_and_insert_plans(request: repayment_schema.AnalyzeAndInsertPlansRequest, db: Session = Depends(get_db)):
    user_id = request.user_id
    loan_amount = request.loan_amount
    interest_rate = request.interest_rate
    duration = request.duration
    month = request.month

    # 사용자 필수 데이터 확인
    if not user_id or not loan_amount:
        raise HTTPException(status_code=400, detail="필수 필드가 누락되었습니다.")

    # 사용자 지출 데이터 조회
    user_expenses = repayment_crud.get_user_expenses(db, user_id, month)
    if not user_expenses:
        raise HTTPException(status_code=404, detail="사용자의 지출 데이터를 찾을 수 없습니다.")

    expense_data = [
        {
            "category_id": expense.category_id,
            "original_amount": expense.original_amount,
            "is_hard_to_reduce": expense.is_hard_to_reduce,
        }
        for expense in user_expenses
    ]

    # GPT 분석 요청
    prompt = gpt_service.generate_prompt_with_loan_details(expense_data, loan_amount, interest_rate, duration)
    gpt_response = gpt_service.call_chatgpt(prompt)
    plans = gpt_service.parse_gpt_response(gpt_response)

    # 분석된 계획 저장
    try:
        repayment_crud.insert_repayment_plans(db, user_id, plans)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 삽입 오류: {e}")

    return {
        "status": "success",
        "message": "상환 계획이 생성되었습니다.",
        "plans": plans
    }

# 2-3. 상환 플랜 리스트 조회
@router.get(
    "/plans"
)
async def repayment_plans(
        user_id: int = Query(1, description="User ID to fetch plans for"),
        db: Session = Depends(get_db)
):
    try:
        plans = repayment_crud.get_repayment_plans(db, user_id)
        return {
            "status": "success",
            "plans": plans
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# 2-3-1. 상환 플랜 상세 조회
@router.get(
    "/plans/{plan_id}"
)
async def repayment_plan_detail(
        plan_id: int,
        user_id: int = Query(1, description="User ID to fetch plans for"),
        db: Session = Depends(get_db)
):
    try:
        plan = repayment_crud.get_repayment_plan(db, plan_id=plan_id, user_id=user_id)
        return {
            "status": "success",
            "plan": plan
        }
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# 2-4. 상환 플랜 선택
@router.post("/select-plan", response_model=PostResponse)
async def repayment_plan_select(
        user_id: int = Query(1, description="User ID to fetch plans for"),
        plan_id: int = Query(1, description="plan ID to fetch plans for"),
        db: Session = Depends(get_db)
):
    try:
        message = repayment_crud.select_repayment_plan(
            db=db,
            user_id=user_id,
            plan_id=plan_id
        )

        return {
            "status": "success",
            "message": message
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
