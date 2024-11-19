#1. OpenAI의 ChatGPT API 호출하는 로직
import openai
import json
from sqlalchemy import func, extract
from .models import UserExpenses, Categories
from .models import Transactions
from .models import User, RepaymentHistory, RepaymentPlans
from . import db
import json
import re
from dotenv import load_dotenv
import os
# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 읽기
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_gpt_response(response_text):
    try:
        # JSON 배열을 추출하기 위해 기본 JSON 패턴 사용
        json_start = response_text.find("[")
        json_end = response_text.rfind("]") + 1

        if json_start == -1 or json_end == -1:
            raise ValueError("응답에 JSON 배열이 포함되어 있지 않습니다.")

        json_str = response_text[json_start:json_end]
        plans = json.loads(json_str)

        # 각 플랜의 details 필드를 문자열로 저장
        for plan in plans:
            if "details" in plan:
                plan["details"] = json.dumps(plan["details"])

        return plans
    except Exception as e:
        raise Exception(f"GPT 응답 파싱 실패: {str(e)}")



def call_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            ## model="gpt-3.5-turbo",
            model="gpt-4o",
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 재무 계획 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=1000
        )
        response_content = response['choices'][0]['message']['content']
        print("ChatGPT Response:", response_content)  # 응답 출력
        return response_content
    except openai.error.RateLimitError as e:
        raise Exception("API 사용 한도를 초과했습니다. OpenAI 계정의 사용량과 요금제를 확인하세요.")
    except openai.error.AuthenticationError as e:
        raise Exception("API 키가 유효하지 않습니다. OpenAI 계정에서 올바른 API 키를 확인하세요.")
    except openai.error.OpenAIError as e:
        raise Exception(f"ChatGPT API 호출 실패: {str(e)}")
    
    
def generate_prompt_with_loan_details(user_expenses, loan_amount, interest_rate, duration):
    # 대출 정보 계산
    monthly_principal = loan_amount / duration  # 월 원금
    monthly_interest = (loan_amount * (interest_rate / 100)) / 12  # 월 이자
    monthly_payment = int(monthly_principal + monthly_interest)  # 월 상환액 (정수로 변환)

    # 사용자 소비 데이터 정리
    expense_summary = [
        f"카테고리 ID: {expense['category_id']}, 금액: {expense['original_amount']}, 절약 어려움: {expense['is_hard_to_reduce']}"
        for expense in user_expenses
    ]

    # 플랜 이름 및 해시태그 정의
    plans_and_hashtags = {
        "쇼핑 절약 플랜": ["#있는거쓰자", "#같은거입어", "#ootd:스티브잡스", "#옷장을열어봐"],
        "식비 절약 플랜": ["#냉장고파먹기", "#배달금지", "#백종원레시피"],
        "문화생활 절약 플랜": ["#산책가자", "#친구OTT같이보자", "#집에서노래나듣자"]
    }

    # 프롬프트 생성
    prompt = f"""
사용자는 대출 {loan_amount:,}원을 이자율 {interest_rate}%로 상환 기간 {duration}개월 동안 갚으려 합니다.
이를 위해 사용자가 매달 갚아야 하는 총 금액은 다음과 같습니다:
- 월 원금: {monthly_principal:,.0f}원
- 월 이자: {monthly_interest:,.0f}원
- **총 월 상환 금액: {monthly_payment:,}원**

사용자의 소비 내역은 다음과 같습니다:
{chr(10).join(expense_summary)}

**플랜 이름 및 해시태그**:
{chr(10).join([f"{i+1}. {plan_name}: {', '.join(hashtags)}" for i, (plan_name, hashtags) in enumerate(plans_and_hashtags.items())])}

**요청사항**:
1. 각 플랜의 `details`에서 `reduced_amount`의 합계는 반드시 `total_amount`인 {monthly_payment:,}원이 되어야 합니다.
2. `category_id = 3`는 각 플랜에서 `total_amount`의 최소 40% 이상을 차지해야 합니다.
3. 남은 금액은 다른 카테고리에서 `original_amount`를 초과하지 않는 선에서 균등 분배하세요.
4. 모든 `saving_percentage` 값은 50%를 초과하지 않도록 제한하세요.
5. 가능한 잔여 금액(합계가 정확히 맞지 않는 경우)은 마지막 항목에서 조정하여 합계를 정확히 맞추세요.
6. details에는 요소가 3개에서 4개로 구성되어야한다.


**반환 형식 예시**:
```json
[
    {{
        "plan_name": "쇼핑 절약 플랜",
        "total_amount": {monthly_payment},
        "duration": {duration},
        "details": [
            {{"category_id": 3, "reduced_amount": 400000, "saving_percentage": 40}},
            {{"category_id": 4, "reduced_amount": 115000, "saving_percentage": 20}}
        ],
        "hashtags": ["#있는거쓰자", "#같은거입어", "#ootd:스티브잡스"]
    }}
]
위 조건을 충족하는 절약 계획 3개를 생성하세요. """ 
    return prompt