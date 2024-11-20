#services.py
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

# 2-2. 줄이기 어려운 카테고리와 상환 기간 저장
def save_repayment_plan(user_id, categories, repayment_period):
    try:
        # 사용자 유효성 검사
        user = User.query.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}, 404

        # 상환 기간 업데이트
        user.repayment_period = repayment_period
        db.session.commit()

        # monthly_repayment_goal 계산
        if user.loan_amount and repayment_period:
            user.monthly_repayment_goal = user.loan_amount // repayment_period  # 정수로 저장
        else:
            return {"status": "error", "message": "Invalid loan amount or repayment period"}, 400

        db.session.commit()  # Users 테이블 업데이트


        # 카테고리별 줄이기 어려운 항목 업데이트
        for category in categories:
            category_name = category["category"]
            is_hard_to_reduce = category["isHardToReduce"]

            # 카테고리 ID 가져오기
            category_obj = Categories.query.filter_by(category_name=category_name).first()
            if not category_obj:
                return {"status": "error", "message": f"Category '{category_name}' not found"}, 404

            # UserExpenses 업데이트 또는 생성
            user_expense = UserExpenses.query.filter_by(
                user_id=user_id,
                category_id=category_obj.category_id
            ).first()

            if user_expense:
                user_expense.is_hard_to_reduce = is_hard_to_reduce
            else:
                new_expense = UserExpenses(
                    user_id=user_id,
                    category_id=category_obj.category_id,
                    month=11,  # 기본값으로 '0' (전체)
                    original_amount=0,  # 초기 값 0
                    is_hard_to_reduce=is_hard_to_reduce
                )
                db.session.add(new_expense)

        db.session.commit()

        return {"status": "success", "message": "상환 계획이 저장되었습니다."}, 200
    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500


#2-3. 상환 플랜 리스트 조회
def get_repayment_plans(user_id):
    """
    Fetch repayment plans for a specific user with suggested savings per category.
    """
    # Query repayment plans for the user
    plans = db.session.query(RepaymentPlans).filter_by(user_id=user_id).all()
    if not plans:
        return []

    plans_data = []
    for plan in plans:
        try:
            # Parse plan details
            plan_details = plan.details if isinstance(plan.details, list) else json.loads(plan.details)

            # Enrich plan details with category names
            categories = []
            for detail in plan_details:
                category = db.session.query(Categories).filter_by(category_id=detail["category_id"]).first()
                if category:
                    categories.append({
                        "categoryId": category.category_id,
                        "categoryName": category.category_name,
                        "suggestedSaving": detail.get("reduced_amount", 0),
                        "savingPercentage": detail.get("saving_percentage", 0.0)
                    })

            # Add plan information
            plans_data.append({
                "planId": plan.plan_id,
                "monthlyPayment": plan.total_amount // plan.duration,
                "duration": plan.duration,
                "description": plan.plan_name,
                "categories": categories,
                "hashtags" : plan.hashtags
            })
        except Exception as e:
            print(f"Error processing plan {plan.plan_id}: {e}")
            continue

    return plans_data

# 2-4. 상환 플랜 선택
def select_repayment_plan(user_id, plan_id):
    """
    Select a repayment plan for the given user.
    """

    user = db.session.query(User).filter_by(user_id=user_id).first()
    if not user:
        raise ValueError("User not found.")

    plan = db.session.query(RepaymentPlans).filter_by(plan_id=plan_id).first()
    if not plan:
        raise ValueError("Repayment plan not found.")

    if plan.user_id != user_id:
        raise ValueError("The selected plan does not belong to this user.")

    user.selected_plan_group_id = plan.plan_id
    db.session.commit()

    return "선택한 상환 플랜이 시작되었습니다."


# 3-1. 상환 요약 조회
def get_dashboard_summary(user_id):
    summary = []

    # Group transactions by month for the given user
    monthly_transactions = db.session.query(
        func.date_format(Transactions.transaction_date, '%Y-%m').label('month'),
        func.sum(Transactions.amount).label('totalSpent')
    ).filter(
        Transactions.user_id == user_id,  # Filter by user_id
        ~Transactions.category_id.in_([1, 2])  # Exclude category_id 1 and 2
    ).group_by('month').all()

    for month, totalSpent in monthly_transactions:
        # Ensure totalSpent is an integer
        totalSpent = int(totalSpent) if totalSpent is not None else 0

        # Fetch transactions for the month, sorted by date
        transactions = db.session.query(
            Transactions.transaction_date,
            Categories.category_name,
            Transactions.description,
            Transactions.amount
        ).join(
            Categories, Transactions.category_id == Categories.category_id
        ).filter(
            Transactions.user_id == user_id,  # Filter by user_id
            func.date_format(Transactions.transaction_date, '%Y-%m') == month
        ).order_by(Transactions.transaction_date).all()

        # Group transactions by category
        categories = db.session.query(
            Categories.category_name.label('category'),
            func.sum(Transactions.amount).label('totalAmount')
        ).join(
            Categories, Transactions.category_id == Categories.category_id
        ).filter(
            Transactions.user_id == user_id,  # Filter by user_id
            func.date_format(Transactions.transaction_date, '%Y-%m') == month
        ).group_by(Categories.category_name).all()

        # Convert category amounts to integers
        categories_data = [
            {"category": c.category, "totalAmount": int(c.totalAmount) if c.totalAmount is not None else 0}
            for c in categories
        ]

        summary.append({
            "month": month,
            "totalSpent": totalSpent,
            "categories": categories_data,
            "transactions": [
                {
                    "date": t.transaction_date.strftime('%Y-%m-%d'),
                    "category": t.category_name,
                    "description": t.description,
                    "amount": int(t.amount)  # Ensure transaction amount is an integer
                } for t in transactions
            ]
        })

    return summary



# 3-2. 상환 현황 조회
def get_repayment_status(user_id):
    # 사용자 대출 정보 가져오기
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # 총 대출 금액과 이자율
    loan_amount = user.loan_amount
    interest_rate = user.interest_rate
    monthly_interest = (loan_amount * (interest_rate / 100)) / user.repayment_period  # 월이자

    # 상환 상태 계산
    total_paid = db.session.query(
        func.sum(RepaymentHistory.repayment_amount)
    ).filter(RepaymentHistory.user_id == user_id).scalar() or 0
    remaining_amount = loan_amount - total_paid

    # 월별 상환 내역
    repayment_chart = db.session.query(
        func.date_format(RepaymentHistory.repayment_date, '%Y-%m').label('month'),
        func.sum(RepaymentHistory.repayment_amount).label('paid')
    ).filter(RepaymentHistory.user_id == user_id) \
     .group_by('month') \
     .order_by('month') \
     .all()

    # 월별 데이터 생성
    repayment_chart_data = [
        {"month": row.month, "paid": row.paid, "interest": round(monthly_interest)}
        for row in repayment_chart
    ]

    # 최종 데이터 반환
    return {
        "repaymentStatus": {
            "totalAmount": loan_amount,
            "paidAmount": total_paid,
            "remainingAmount": remaining_amount
        },
        "repaymentChart": repayment_chart_data
    }

# 3-3. 상환 플랜 비율 조회
def get_consumption_percentage(user_id):
    # 사용자와 선택된 플랜 가져오기
    user = db.session.query(User).filter(User.user_id == user_id).first()

    if not user:
        return {"status": "error", "message": "User not found"}, 404

    if not user.selected_plan_group_id:
        return {"status": "error", "message": "No repayment plan selected for the user"}, 404

    plan = db.session.query(RepaymentPlans).filter(RepaymentPlans.plan_id == user.selected_plan_group_id).first()

    if not plan:
        return {"status": "error", "message": "Repayment plan not found"}, 404

    # 플랜 정보
    plan_name = plan.plan_name
    total_amount = plan.total_amount
    duration = plan.duration
    hashtags = plan.hashtags

    # 플랜 상세 데이터 (details)
    plan_details = plan.details
    if isinstance(plan_details, str):
        try:
            plan_details = json.loads(plan_details)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON format in plan details"}, 500

    # 카테고리별 데이터 구성
    categories = []
    for entry in plan_details:
        category_id = entry.get("category_id")
        saving_percentage = entry.get("saving_percentage")

        # 카테고리 이름 조회
        category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
        if category:
            categories.append({
                "category_id": category_id,
                "category_name": category.category_name,
                "saving_percentage": saving_percentage
            })

    # 최종 응답 데이터
    return {
        "status": "success",
        "data": {
            "selectedPlanName": plan_name,
            "total_amount": total_amount,
            "duration": duration,
            "categories": categories,
            "hashtags": hashtags
        }
    }


# 3-4. 소비 분석 조회
def get_consumption_analysis(user_id):
    # 사용자와 선택된 상환 플랜 가져오기
    user = db.session.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"status": "error", "message": "User not found"}, 404

    if not user.selected_plan_group_id:
        return {"status": "error", "message": "No repayment plan selected for the user"}, 404

    plan = db.session.query(RepaymentPlans).filter(RepaymentPlans.plan_id == user.selected_plan_group_id).first()
    if not plan:
        return {"status": "error", "message": "Repayment plan not found"}, 404

    # 데이터가 JSON 문자열인지 확인하고 로드
    if isinstance(plan.details, str):
        try:
            plan_details = json.loads(plan.details)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON format in plan details"}, 500
    elif isinstance(plan.details, list):  # 이미 리스트인 경우 처리
        plan_details = plan.details
    else:
        return {"status": "error", "message": "Invalid plan details format"}, 500

    # UserExpenses에서 10월과 11월 데이터를 가져오기
    october_expenses = db.session.query(
        UserExpenses.category_id,
        UserExpenses.original_amount
    ).filter(
        UserExpenses.user_id == user_id,
        UserExpenses.month == 10
    ).all()

    november_expenses = db.session.query(
        UserExpenses.category_id,
        UserExpenses.original_amount
    ).filter(
        UserExpenses.user_id == user_id,
        UserExpenses.month == 11
    ).all()

    # 데이터를 카테고리 ID를 키로 하는 딕셔너리로 변환
    october_expenses_dict = {expense.category_id: expense.original_amount for expense in october_expenses}
    november_expenses_dict = {expense.category_id: expense.original_amount for expense in november_expenses}

    # 소비 분석 데이터 생성
    categories_data = []
    for entry in plan_details:
        category_id = entry.get("category_id")
        reduced_amount = entry.get("reduced_amount", 0)

        # 10월 사용 금액 및 절약 목표 계산
        october_amount = october_expenses_dict.get(category_id, 0)
        suggested_reduced_amount = max(october_amount - reduced_amount, 0)

        # 11월 사용 금액 가져오기
        november_amount = november_expenses_dict.get(category_id, 0)

        # 절약 비율 계산
        saving_percentage = (november_amount / suggested_reduced_amount) * 100 if reduced_amount else 0

        # 카테고리 이름 가져오기
        category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
        category_name = category.category_name if category else "Unknown"

        categories_data.append({
            "category": category_name,
            "amount": november_amount,
            "suggestedReducedAmount": suggested_reduced_amount,
            "savingPercentage": round(saving_percentage, 2)
        })

    return {
        "month": "2024-11",
        "totalAmount": sum(november_expenses_dict.values()),
        "categories": categories_data
    }

# 4. 거래내역 추가
def create_transaction_service(user_id, category_id, transaction_date, amount, description, payment_method):
    """
    거래내역을 생성하는 서비스 함수
    """
    try:
        # 새로운 거래 추가
        transaction = Transactions(
            user_id=user_id,
            category_id=category_id,
            transaction_date=transaction_date,
            amount=amount,
            description=description,
            payment_method=payment_method
        )
        db.session.add(transaction)
        db.session.commit()

        return {"status": "success", "message": "Transaction created successfully"}, 201

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500
    

    # 5-2. 새 알림 생성
    