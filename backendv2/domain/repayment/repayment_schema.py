from pydantic import BaseModel
from typing import List, Optional

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
class RepaymentPlanRequest(BaseModel):
    userId: int
    categories: List[int]
    repaymentPeriod: int

class ResponseModel(BaseModel):
    status: str
    message: str

#2-3. 상환 플랜 리스트 조회
class CategoryDetail(BaseModel):
    categoryId: int
    reducedAmount: float
    savingPercentage: float

class RepaymentPlan(BaseModel):
    planId: int
    monthlyPayment: int
    duration: int
    description: str
    categories: List[CategoryDetail]
    hashtags: str

class RepaymentPlansListResponse(BaseModel):
    status: str
    plans: List[RepaymentPlan]