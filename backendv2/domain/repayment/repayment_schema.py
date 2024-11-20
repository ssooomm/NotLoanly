from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
class RepaymentPlanRequest(BaseModel):
    userId: int
    categories: List[int]
    repaymentPeriod: int

class ResponseModel(BaseModel):
    status: str
    message: str

#2-3. 상환 플랜 리스트 조회
class RepaymentPlan(BaseModel):
    planId: int
    planName: str
    totalAmount: int
    duration: int
    details: Dict[str,Any]
    hashtags: str

