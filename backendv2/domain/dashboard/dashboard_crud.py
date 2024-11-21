from typing import Dict

from domain.dashboard.dashboard_schema import *
from domain.repayment.repayment_schema import Plan_Details
from models import Transactions, Categories, RepaymentHistory, UserExpenses

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from domain.common.common_crud import get_user
from domain.repayment.repayment_crud import get_repayment_plan
from fastapi import HTTPException
import json
import datetime
from datetime import datetime


# 3-1. 상환 요약 조회
def get_dashboard_summary(db: Session, user_id: int) -> SummaryResponse:
    summary = []

    # Group transactions by month for the given user, excluding income categories for totalSpent
    monthly_transactions = db.query(
        func.date_format(Transactions.transaction_date, '%Y-%m').label('month'),
        func.sum(case(
            (Transactions.category_id.notin_([1, 2]), Transactions.amount),
            else_=0
        )).label('totalSpent')
    ).filter(
        Transactions.user_id == user_id
    ).group_by('month').all()

    for month, totalSpent in monthly_transactions:
        totalSpent = int(totalSpent) if totalSpent is not None else 0

        # Fetch all transactions for the month (including income)
        transactions = db.query(
            Transactions.transaction_date,
            Categories.category_name,
            Transactions.description,
            Transactions.amount
        ).join(
            Categories, Transactions.category_id == Categories.category_id
        ).filter(
            Transactions.user_id == user_id,
            func.date_format(Transactions.transaction_date, '%Y-%m') == month
        ).order_by(Transactions.transaction_date).all()

        # Map transactions to TransactionBase objects
        transaction_objects = [
            TransactionBase(
                date=t.transaction_date.strftime('%Y-%m-%d'),
                category=t.category_name,
                description=t.description,
                amount=int(t.amount)
            ) for t in transactions
        ]

        # Group all transactions by category (including income)
        categories = db.query(
            Categories.category_name.label('category'),
            func.sum(Transactions.amount).label('totalAmount')
        ).join(
            Categories, Transactions.category_id == Categories.category_id
        ).filter(
            Transactions.user_id == user_id,
            func.date_format(Transactions.transaction_date, '%Y-%m') == month
        ).group_by(
            Categories.category_name
        ).all()

        # Map categories to CategorySummary objects
        category_summaries = [
            CategorySummary(
                category=c.category,
                totalAmount=int(c.totalAmount) if c.totalAmount is not None else 0
            ) for c in categories
        ]

        # Create MonthlySummary object for the month
        monthly_summary = MonthlySummary(
            month=month,
            totalSpent=totalSpent,
            categories=category_summaries,
            transactions=transaction_objects
        )

        summary.append(monthly_summary)

    # Create SummaryResponse object
    response = SummaryResponse(
        status="success",
        summary=summary
    )

    return response


# 3-2. 상환 현황 조회
def get_repayment_status(db: Session, user_id: int):  # -> RepaymentStatusResponse
    # 사용자 대출 정보 가져오기
    user = get_user(db, user_id)
    if not user:
        raise ValueError("User not found")

    loan_amount = user.loan_amount  # 총 대출 금액
    interest_rate = user.interest_rate  # 이자율
    repayment_period = user.repayment_period # 상환 기간

    # 상환 상태 계산 paidAmount
    total_paid = db.query(
        func.sum(RepaymentHistory.repayment_amount)
    ).filter(RepaymentHistory.user_id == user_id).scalar() or 0

    repayment_history = db.query(RepaymentHistory).filter(
        RepaymentHistory.user_id == user_id
    ).order_by(
        desc(RepaymentHistory.repayment_date)
    ).all()
    total_count = len(repayment_history)

    remaining_amount = loan_amount - total_paid
    total_paid_percenatage = (total_count /repayment_period) * 100

    return {
            "repayment_period": repayment_period,
            "loan_amount": loan_amount,
            "remaining_amount": remaining_amount,
            "total_paid_percenatage": round(total_paid_percenatage, 2),
            "total_paid": total_paid,
            "total_count": total_count,
            "repayment_amount":repayment_history[0].repayment_amount,
            "interest_amount":repayment_history[0].interest_amount
        }


# 3-3 상환 플랜 비율 조회
def get_consumption_percentage(db: Session, user_id: int):
    # 사용자 조회
    user = get_user(db, user_id)
    if not user:
        return {"status": "error", "message": "User not found"}, 404

    if not user.selected_plan_group_id:
        return {"status": "error", "message": "No repayment plan selected for the user"}, 404

    # 플랜 조회
    plan = get_repayment_plan(db, user.selected_plan_group_id, user_id)
    # plan = db.query(RepaymentPlans).filter(RepaymentPlans.plan_id == user.selected_plan_group_id).first()
    if not plan:
        return {"status": "error", "message": "Repayment plan not found"}, 404

    # 플랜 정보 파싱
    plan_details = plan.details
    if isinstance(plan_details, str):
        try:
            plan_details = json.loads(plan_details)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON format in plan details"}, 500

    # 카테고리 데이터 구성
    categories = []
    for entry in plan_details:
        category_id = entry.get("category_id")
        saving_percentage = entry.get("saving_percentage")

        category = db.query(Categories).filter(Categories.category_id == category_id).first()
        if category:
            categories.append({
                "category_id": category_id,
                "category_name": category.category_name,
                "saving_percentage": saving_percentage
            })

    return {
        "status": "success",
        "data": {
            "selectedPlanName": plan.plan_name,
            "total_amount": plan.total_amount,
            "duration": plan.duration,
            "categories": categories,
            "hashtags": plan.hashtags
        }
    }


# 3-4. 소비 분석 조회
def get_consumption_analysis(db: Session, user_id: int, month: int):
    # 사용자 조회
    user = get_user(db, user_id)
    if not user:
        return {"status": "error", "message": "User not found"}, 404

    if not user.selected_plan_group_id:
        return {"status": "error", "message": "No repayment plan selected for the user"}, 404

    # 플랜 조회
    plan = get_repayment_plan(db, user.selected_plan_group_id, user_id)
    if not plan:
        return {"status": "error", "message": "Repayment plan not found"}, 404
    plan_details = plan.details

    # 주어진 month에 해당하는 지출 조회
    expenses = get_user_expenses_by_month(db, user_id, month)
    if not expenses:
        return {"status": "error", "message": "Expenses not found"}, 404

    categories = generate_categories_summary(expenses, plan_details)

    return {
        "month": month,
        "totalAmount": sum(expense["total_amount"] for expense in expenses),
        "categories": categories
    }


# user_id와 month에 해당하는 UserExpenses 데이터를 조회
def get_user_expenses_by_month(db: Session, user_id: int, month: int):
    expenses = db.query(
        UserExpenses.category_id,
        UserExpenses.original_amount
    ).filter(
        UserExpenses.user_id == user_id,
        UserExpenses.month == month
    ).all()

    # 결과를 딕셔너리 형태로 변환
    return [
        {"category_id": category_id, "total_amount": original_amount}
        for category_id, original_amount in expenses
    ]


def generate_categories_summary(expenses, plan_details):
    # expenses를 딕셔너리로 변환하여 빠르게 접근할 수 있도록 설정
    expenses_dict = {expense["category_id"]: expense["total_amount"] for expense in expenses}

    # 결과 리스트 생성
    categories = []

    for plan in plan_details:
        category_id = plan["category_id"]
        reduced_amount = plan["reduced_amount"]
        original_amount = plan["original_amount"]
        # saving_percentage = round(plan["saving_percentage"], 2)

        # expenses에서 category_id에 해당하는 total_amount 가져오기
        amount = expenses_dict.get(category_id, 0)  # 기본값은 0
        suggested_reduced_amount = original_amount - reduced_amount
        using_percentage = round((amount / suggested_reduced_amount) * 100, 2)

        # 결과에 추가
        categories.append({
            "category_id": category_id,
            "amount": amount,
            "suggestedReducedAmount": suggested_reduced_amount,
            "usingPercentage": using_percentage
        })

    return categories
