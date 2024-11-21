from sqlalchemy.orm import Session
from fastapi import HTTPException
from domain.common.common_crud import get_user, get_user_name, get_category_name
from domain.dashboard.dashboard_crud import get_user_expenses_by_month
from domain.repayment.repayment_crud import get_repayment_plan
from shared_memory import notifications
from models import Transactions, Notification, User
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.sql import text


class TransactionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_notifications(self, user_id: int):
        """
        특정 사용자(user_id)의 알림을 조회합니다.
        """
        try:
            notifications = self.db.query(Notification).filter(Notification.user_id == user_id).all()
            if not notifications:
                return []
            return [
                {
                    "notification_id": n.notification_id,
                    "message": n.message,
                    "sent_at": n.sent_at.strftime('%Y-%m-%d %H:%M:%S') if n.sent_at else None,
                }
                for n in notifications
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")


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

    def get_users_with_loan_due_tomorrow(self):
        """
        하루 전 상환일이 다가온 사용자를 검색합니다.
        """
        today = datetime.now()
        tomorrow = today + timedelta(days=1)

        # 내일 상환일인 사용자 검색
        users = self.db.query(User).filter(
            func.date(User.loan_date) == tomorrow.date()
        ).all()
        return users

    def get_users_with_upcoming_repayment(self):
        """
        상환 주기에 따라 상환일이 다가온 사용자를 검색합니다.
        """
        now = datetime.now()
        tomorrow = now + timedelta(days=1)

        users = self.db.query(User).filter(
            func.date_add(
                func.date(User.loan_date),
                func.interval(
                    func.timestampdiff(text("MONTH"), User.loan_date, now) + 1,
                    text("MONTH")
                )
            ) == tomorrow.date()
        ).all()

        return users


    def get_users_with_upcoming_repayment(self):
        """
        상환 주기에 따라 상환일이 다가온 사용자를 검색합니다.
        """
        now = datetime.now()
        tomorrow = now + timedelta(days=1)

        try:
            # Raw SQL을 사용한 대출 상환일 계산
            query = text("""
                SELECT *
                FROM users
                WHERE DATE_ADD(
                    DATE(users.loan_date),
                    INTERVAL TIMESTAMPDIFF(MONTH, users.loan_date, :current_date) + 1 MONTH
                ) = :tomorrow
            """)

            users = self.db.execute(query, {
                "current_date": now.date(),
                "tomorrow": tomorrow.date()
            }).fetchall()

            return users

        except Exception as e:
            print(f"Error querying upcoming repayment users: {str(e)}")
            return []




    def send_repayment_reminder_notifications(self):
        """
        상환일 알림을 전송합니다.
        """
        users = self.get_users_with_upcoming_repayment()
        if not users:
            print("No users with loan repayment due tomorrow.")
            return

        for user in users:
            message = f"{user.name}님, 대출 상환일이 내일입니다. 준비해주세요!"
            print(f"Sending notification to {user.name}: {message}")

            # 알림 데이터 저장
            notification = Notification(
                user_id=user.user_id,
                message=message
            )
            self.db.add(notification)

        self.db.commit()
        result_message = f"Sent reminders to {len(users)} users."
        print(result_message)
        return result_message

