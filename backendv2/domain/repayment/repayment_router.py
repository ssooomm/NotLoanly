from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from domain.repayment import repayment_schema, repayment_crud

router = APIRouter(
    prefix="/api/repayment",
)

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
@router.post("/repayment/save-plan", response_model=repayment_schema.ResponseModel)
async def save_plan(
    plan: repayment_schema.RepaymentPlanRequest,
    db: Session = Depends(get_db)
) -> repayment_schema.ResponseModel:
    try:
        result = repayment_crud.save_repayment_plan(
            db,
            user_id=plan.userId,
            category_ids=plan.categories,
            repayment_period=plan.repaymentPeriod
        )
        return result
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

#2-3. 상환 플랜 리스트 조회
@router.get(
    "/plans"
)
async def get_repayment_plans(
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