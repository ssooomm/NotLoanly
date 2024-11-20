from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.repayment import repayment_schema, repayment_crud

router = APIRouter(
    prefix="/api/loan",
)

# 1-1. 대출 신청

# 1-2. GPT 호출
