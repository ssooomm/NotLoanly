from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from domain.notification.notification_schema import TransactionCreate
from models import Transactions, Notification, User, RepaymentPlans, UserExpenses, Categories, User
import json
from shared_memory import notifications  # 공유 메모리 임포트


class TransactionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, transaction: TransactionCreate) -> bool:
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

            # 절약 비율 확인 및 알림 처리 호출 (추가된 카테고리에 대해서만)
            self.check_saving_percentage_and_notify(transaction.user_id, transaction.category_id)

            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")

    

    def get_user_notifications(self, user_id: int):
        try:
            notifications = self.db.query(Notification).filter(Notification.user_id == user_id).all()
            if not notifications:
                return []
            return [
                {"notification_id": n.notification_id, "message": n.message, "sent_at": n.sent_at}
                for n in notifications
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")

    def create_transaction_notification(self, user_id: int, category_id: int, saving_percentage: float, category_name: str, message: str):
        """
        알림 메시지를 SSE 큐 및 DB에 추가
        """
        print(f"Adding notification: {message}")  # 디버깅용 출력
        
        # SSE 큐에 추가
        #notifications.append(message)
        # SSE 큐에 JSON 데이터 추가
        notifications.append({"user_id": user_id, "message": message})

        # DB에 알림 저장
        db_notification = Notification(
            user_id=user_id,
            message=message
        )
        self.db.add(db_notification)
        self.db.commit()


    def check_saving_percentage_and_notify(self, user_id: int, category_id: int):
        # 사용자 조회
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.selected_plan_group_id:
            raise HTTPException(status_code=404, detail="No repayment plan selected for the user")

        # 플랜 조회
        plan = self.db.query(RepaymentPlans).filter(RepaymentPlans.plan_id == user.selected_plan_group_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Repayment plan not found")

        # 플랜 세부 정보 파싱
        try:
            plan_details = json.loads(plan.details) if isinstance(plan.details, str) else plan.details
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON format in plan details")

        if not isinstance(plan_details, list):
            raise HTTPException(status_code=500, detail="Invalid plan details format")

        # 거래 내역이 추가된 카테고리에 해당하는 플랜 정보 가져오기
        category_plan = next((entry for entry in plan_details if entry.get("category_id") == category_id), None)
        if not category_plan:
            return  # 해당 카테고리가 플랜에 포함되지 않은 경우 처리하지 않음

        reduced_amount = category_plan.get("reduced_amount", 0)

        # 10월 소비 금액 및 절약 목표 계산
        october_expense = self.db.query(UserExpenses.original_amount).filter(
            UserExpenses.user_id == user_id,
            UserExpenses.category_id == category_id,
            UserExpenses.month == 10
        ).scalar() or 0
        suggested_reduced_amount = max(october_expense - reduced_amount, 0)

        # 11월 소비 금액 가져오기
        november_expense = self.db.query(UserExpenses.original_amount).filter(
            UserExpenses.user_id == user_id,
            UserExpenses.category_id == category_id,
            UserExpenses.month == 11
        ).scalar() or 0

        # 절약 비율 계산
        saving_percentage = (november_expense / suggested_reduced_amount) * 100 if suggested_reduced_amount else 0

        # 카테고리 이름 가져오기
        category = self.db.query(Categories).filter(Categories.category_id == category_id).first()
        category_name = category.category_name if category else "Unknown"

        # 메시지 생성 및 알림 처리
        if saving_percentage >= 80:
            if saving_percentage < 100:
                # 80% 이상, 100% 미만
                message = f"{user.name}님, {category_name} 부분에서 {round(saving_percentage)}% 사용했습니다. 한 발짝만 더 절약해볼까요?"
            elif saving_percentage == 100:
                # 정확히 100%
                message = f"{user.name}님, {category_name} 부분에서 100% 사용했습니다. 목표 금액을 다 사용했습니다."
            else:
                # 100% 초과
                overused_percentage = round(saving_percentage - 100, 2)
                message = f"{user.name}님, {category_name} 부분에서 계획보다 {overused_percentage}% 더 사용했습니다."

            # 알림 전송 및 저장
            self.create_transaction_notification(user_id, category_id, saving_percentage, category_name, message)
