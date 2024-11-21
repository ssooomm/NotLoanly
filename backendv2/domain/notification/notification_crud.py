from sqlalchemy.orm import Session
from fastapi import HTTPException
from domain.common.common_crud import get_user, get_user_name, get_category_name
from domain.dashboard.dashboard_crud import get_user_expenses_by_month
from domain.repayment.repayment_crud import get_repayment_plan
from shared_memory import notifications
from models import Transactions, Notification
from datetime import datetime


class TransactionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, transaction):
        try:
            db_transaction = Transactions(
                user_id=transaction.user_id,
                category_id=transaction.category_id,
                transaction_date=transaction.transaction_date,
                amount=transaction.amount,
                description=transaction.description,
                payment_method=transaction.payment_method
            )
            self.db.add(db_transaction)
            self.db.commit()
            self.db.refresh(db_transaction)

            # 절약 비율 확인 및 알림 처리
            self.check_saving_percentage_and_notify(transaction.user_id, transaction.category_id)

            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")

    def check_saving_percentage_and_notify(self, user_id: int, category_id: int):
        user_name = get_user_name(self.db, user_id)
        consumption_data = self.get_consumption_analysis(user_id)
        if consumption_data["status"] == "error":
            return

        category_data = next((c for c in consumption_data["categories"] if c["category_id"] == category_id), None)
        if category_data:
            using_percentage = category_data["usingPercentage"]
            category_name = get_category_name(self.db, category_id)

            message = self.generate_notification_message(user_name, category_name, using_percentage)
            self.create_transaction_notification(user_id, category_id, using_percentage, category_name, message)

    def generate_notification_message(self, user_name: str, category_name: str, using_percentage: float) -> str:
        if using_percentage < 100:
            return f"{user_name}님, {category_name} 부분에서 {round(using_percentage)}% 사용했습니다. 한 발짝만 더 절약해볼까요?"
        elif using_percentage == 100:
            return f"{user_name}님, {category_name} 부분에서 100% 사용했습니다. 목표 금액을 다 사용했습니다."
        else:
            overused_percentage = round(using_percentage - 100, 2)
            return f"{user_name}님, {category_name} 부분에서 계획보다 {overused_percentage}% 더 사용했습니다."

    def create_transaction_notification(self, user_id: int, category_id: int, using_percentage: float, category_name: str, message: str):
        """
        알림 메시지를 SSE 큐 및 DB에 추가
        """
        print(f"Adding notification: {message}")  # 디버깅용 출력

        # SSE 큐에 JSON 데이터 추가
        notifications.append({"user_id": user_id, "message": message})

        # DB에 알림 저장
        db_notification = Notification(
            user_id=user_id,
            message=message
        )
        self.db.add(db_notification)
        self.db.commit()

    def get_consumption_analysis(self, user_id: int):
        user = get_user(self.db, user_id)
        if not user.selected_plan_group_id:
            return {"status": "error", "message": "No repayment plan selected for the user"}

        plan = get_repayment_plan(self.db, user.selected_plan_group_id, user_id)
        if not plan:
            return {"status": "error", "message": "Repayment plan not found"}

        current_month = datetime.now().month
        expenses = get_user_expenses_by_month(self.db, user_id, current_month)
        if not expenses:
            return {"status": "error", "message": "Expenses not found"}

        categories = self.generate_categories_summary(expenses, plan.details)
        return {"status": "success", "categories": categories}

    def generate_categories_summary(self, expenses, plan_details):
        expenses_dict = {e["category_id"]: e["total_amount"] for e in expenses}
        categories = []
        for plan in plan_details:
            category_id = plan["category_id"]
            amount = expenses_dict.get(category_id, 0)
            suggested_reduced_amount = max(plan["original_amount"] - plan["reduced_amount"], 0)
            using_percentage = (amount / suggested_reduced_amount) * 100 if suggested_reduced_amount > 0 else 0

            categories.append({
                "category_id": category_id,
                "amount": amount,
                "suggestedReducedAmount": suggested_reduced_amount,
                "usingPercentage": round(using_percentage, 2),
            })
        return categories
