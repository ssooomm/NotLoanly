from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from domain.dashboard import dashboard_schema, dashboard_crud

# from models import User

router = APIRouter(
    prefix="/api/dashboard",
)


# @router.get("/categories",response_model=List[dashboard_schema.CategorySchema])
# def question_list(db: Session = Depends(get_db)):
#     answer = dashboard_crud.get_existing_user(db)
#     return answer

# 3-1. 상환 요약 조회
@router.get("/summary")
def repayment_summary(user_id: int = Query(1, alias="user_id"),db: Session = Depends(get_db)):
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")

        answer = dashboard_crud.get_dashboard_summary(db, user_id=user_id)

        return answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3-2. 상환 현황 조회
@router.get("/repayment-status")
def repayment_status(user_id: int = Query(1, alias="user_id"),db: Session = Depends(get_db)):
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")

        answer = dashboard_crud.get_repayment_status(db, user_id=user_id)

        return answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3-3 상환 플랜 비율 조회
@router.get(
    "/consumption-percentage"
)
def consumption_percentage(user_id: int, db: Session = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    response = dashboard_crud.get_consumption_percentage(db, user_id=user_id)

    # if response["status"] == "error":
    #     raise HTTPException(status_code=status, detail=response["message"])

    return response

# 3-4. 소비 분석 조회
@router.get(
    "/consumption-analysis")
def consumption_analysis(user_id: int = Query(1, alias="user_id"),db: Session = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    response = dashboard_crud.get_consumption_analysis(db, user_id)

    # if response["status"] == "error":
    #     raise HTTPException(status_code=status, detail=response["message"])

    return response