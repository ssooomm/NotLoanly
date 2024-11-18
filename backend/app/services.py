#services.py
#1. OpenAI의 ChatGPT API 호출하는 로직
import openai
from .models import UserExpenses, Categories
from . import db

# OpenAI API 키 설정
openai.api_key = "your-openai-api-key"

def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"


# 2-1. 소비 분석 데이터 조회
def get_montyly_expense(user_id, month):
    expenses = (
        db.session.query(Categories.category_name, UserExpenses.original_amount)
        .join(Categories, UserExpenses.category_id == Categories.category_id)
        .filter(UserExpenses.user_id == user_id, UserExpenses.month == month)
        .all()
    )
    return{
        "categories": [
            {"category": expense[0], "amount": expense[1]} for expense in expenses
        ]
    }