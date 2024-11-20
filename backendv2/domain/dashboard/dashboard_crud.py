from domain.dashboard.dashboard_schema import *
from models import Transactions, User, Categories, RepaymentHistory, RepaymentPlans, UserExpenses

from sqlalchemy.orm import Session
from sqlalchemy import func
from domain.notification import notification_schema, notification_crud
from domain.common.common_crud import get_user

import json

# 3-1. 상환 요약 조회
def get_dashboard_summary(db: Session, user_id: int) -> SummaryResponse:
    summary = []

    # Group transactions by month for the given user
    monthly_transactions = db.query(
        func.date_format(Transactions.transaction_date, '%Y-%m').label('month'),
        func.sum(Transactions.amount).label('totalSpent')
    ).filter(
        Transactions.user_id == user_id
    ).group_by('month').all()

    for month, totalSpent in monthly_transactions:
        totalSpent = int(totalSpent) if totalSpent is not None else 0

        # Fetch transactions for the month
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

        # Group transactions by category
        categories = db.query(
            Categories.category_name.label('category'),
            func.sum(Transactions.amount).label('totalAmount')
        ).join(
            Categories, Transactions.category_id == Categories.category_id
        ).filter(
            Transactions.user_id == user_id,
            func.date_format(Transactions.transaction_date, '%Y-%m') == month
        ).group_by(Categories.category_name).all()

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
def get_repayment_status(db: Session, user_id: int) -> RepaymentStatusResponse:
    # 사용자 대출 정보 가져오기
    user = get_user(db,user_id)
    if not user:
        raise ValueError("User not found")

    # 총 대출 금액과 이자율
    loan_amount = user.loan_amount
    interest_rate = user.interest_rate
    monthly_interest = (loan_amount * (interest_rate / 100)) / user.repayment_period  # 월이자

    # 상환 상태 계산
    total_paid = db.query(
        func.sum(RepaymentHistory.repayment_amount)
    ).filter(RepaymentHistory.user_id == user_id).scalar() or 0
    remaining_amount = loan_amount - total_paid

    # 월별 상환 내역
    repayment_chart = db.query(
        func.date_format(RepaymentHistory.repayment_date, '%Y-%m').label('month'),
        func.sum(RepaymentHistory.repayment_amount).label('paid')
    ).filter(RepaymentHistory.user_id == user_id) \
        .group_by('month') \
        .order_by('month') \
        .all()

    # 월별 데이터 생성
    repayment_chart_data = [
        {"month": row.month, "paid": row.paid, "interest": round(monthly_interest, 2)}
        for row in repayment_chart
    ]

    # 최종 데이터 반환
    return RepaymentStatusResponse(
        repaymentStatus=RepaymentStatus(
            totalAmount=loan_amount,
            paidAmount=total_paid,
            remainingAmount=remaining_amount
        ),
        repaymentChart=[
            RepaymentChartItem(
                month=item["month"],
                paid=item["paid"],
                interest=item["interest"]
            ) for item in repayment_chart_data
        ]
    )


# 3-3 상환 플랜 비율 조회
def get_consumption_percentage(db: Session, user_id: int):
    # 사용자 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"status": "error", "message": "User not found"}, 404

    if not user.selected_plan_group_id:
        return {"status": "error", "message": "No repayment plan selected for the user"}, 404

    # 플랜 조회
    plan = db.query(RepaymentPlans).filter(RepaymentPlans.plan_id == user.selected_plan_group_id).first()
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
def get_consumption_analysis(db: Session, user_id: int):
    # 사용자 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"status": "error", "message": "User not found"}, 404

    if not user.selected_plan_group_id:
        return {"status": "error", "message": "No repayment plan selected for the user"}, 404

    # 플랜 조회
    plan = db.query(RepaymentPlans).filter(RepaymentPlans.plan_id == user.selected_plan_group_id).first()
    if not plan:
        return {"status": "error", "message": "Repayment plan not found"}, 404

    # 플랜 세부 정보 파싱
    try:
        plan_details = json.loads(plan.details) if isinstance(plan.details, str) else plan.details
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid JSON format in plan details"}, 500

    if not isinstance(plan_details, list):
        return {"status": "error", "message": "Invalid plan details format"}, 500

    # 10월과 11월 소비 데이터 조회
    october_expenses = db.query(UserExpenses.category_id, UserExpenses.original_amount).filter(
        UserExpenses.user_id == user_id, UserExpenses.month == 10
    ).all()

    november_expenses = db.query(UserExpenses.category_id, UserExpenses.original_amount).filter(
        UserExpenses.user_id == user_id, UserExpenses.month == 11
    ).all()

    # 소비 데이터를 딕셔너리로 변환
    october_expenses_dict = {expense.category_id: expense.original_amount for expense in october_expenses}
    november_expenses_dict = {expense.category_id: expense.original_amount for expense in november_expenses}

    # 소비 분석 데이터 생성
    categories_data = []
    for entry in plan_details:
        category_id = entry.get("category_id")
        reduced_amount = entry.get("reduced_amount", 0)

        # 10월 소비 금액 및 절약 목표 계산
        october_amount = october_expenses_dict.get(category_id, 0)
        suggested_reduced_amount = max(october_amount - reduced_amount, 0)

        # 11월 소비 금액 가져오기
        november_amount = november_expenses_dict.get(category_id, 0)

        # 절약 비율 계산
        saving_percentage = (november_amount / suggested_reduced_amount) * 100 if suggested_reduced_amount else 0

        # 카테고리 이름 가져오기
        category = db.query(Categories).filter(Categories.category_id == category_id).first()
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
