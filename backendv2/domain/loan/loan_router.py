from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.loan import loan_crud, loan_schema
from domain.common.common_schema import PostResponse

router = APIRouter(
    prefix="/api/loan",
)

# 1-1. 대출 신청
@router.post(
    "/apply",
    response_model=PostResponse
)
async def loan_apply(
        loan_request: loan_schema.LoanApplicationRequest,
        db: Session = Depends(get_db)
):
    try:
        message = loan_crud.apply_loan(
            db=db,
            req=loan_request
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
# 1-2. GPT 호출
