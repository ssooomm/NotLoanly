from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
class RepaymentPlanRequest(BaseModel):
    user_id: int
    categories: List[int]
    repayment_period: int


# 2-2-1. gpt
class ExpenseData(BaseModel):
    category_id: int
    original_amount: float
    is_hard_to_reduce: bool


class Plan(BaseModel):
    plan_name: str
    total_amount: float
    duration: int
    details: Dict[str, Any]
    hashtags: List[str]


class AnalyzeAndInsertPlansRequest(BaseModel):
    user_id: int
    loan_amount: float
    interest_rate: Optional[float] = 6.0
    duration: Optional[int] = 6
    month: Optional[int] = 10


class AnalyzeAndInsertPlansResponse(BaseModel):
    status: str
    message: str
    plans: List[Plan]

#2-3. 상환 플랜 리스트 조회
class RepaymentPlan(BaseModel):
    plan_id: int
    plan_name: str
    total_amount: int
    duration: int
    details: Dict[str,Any]
    hashtags: str

