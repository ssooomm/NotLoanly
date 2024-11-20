from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# 1-1. 대출 신청 body
class LoanApplicationRequest(BaseModel):
    user_id: int
    loan_amount: int
    interest_rate: float
