from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.repayment import repayment_schema, repayment_crud
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
) -> repayment_schema.ResponseModel:
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
