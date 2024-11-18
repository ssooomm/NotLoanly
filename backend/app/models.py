from . import db
from datetime import datetime

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     # to_dict 메서드는 클래스 내부에 정확히 들여쓰기되어 있어야 합니다.
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "email": self.email
#         }

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    monthly_income = db.Column(db.Integer, nullable=False)
    monthly_expense = db.Column(db.Integer, nullable=False)
    available_funds = db.Column(db.Integer, nullable=False)  # MySQL에선 GENERATED ALWAYS AS 지원 필요
    loan_amount = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    repayment_period = db.Column(db.Integer, nullable=False)
    monthly_repayment_goal = db.Column(db.Integer, nullable=False)
    selected_plan_group_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "monthly_income": self.monthly_income,
            "monthly_expense": self.monthly_expense,
            "available_funds": self.available_funds,
            "loan_amount": self.loan_amount,
            "interest_rate": self.interest_rate,
            "repayment_period": self.repayment_period,
            "monthly_repayment_goal": self.monthly_repayment_goal,
            "selected_plan_group_id": self.selected_plan_group_id,
            "created_at": self.created_at
        }
    


class UserExpenses(db.Model):
    __tablename__ = 'UserExpenses'
    user_expense_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    original_amount = db.Column(db.Integer, nullable=False)
    is_hard_to_reduce = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "user_expense_id": self.user_expense_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "month": self.month,
            "original_amount": self.original_amount,
            "is_hard_to_reduce": self.is_hard_to_reduce
        }


class Categories(db.Model):
    __tablename__ = 'Categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)


class RepaymentPlans(db.Model):
    __tablename__ = 'RepaymentPlans'

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    plan_name = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    details = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            "plan_id": self.plan_id,
            "user_id": self.user_id,
            "plan_name": self.plan_name,
            "total_amount": self.total_amount,
            "duration": self.duration,
            "details": self.details,
            "created_at": self.created_at
        }


# RepaymentHistory 테이블
class RepaymentHistory(db.Model):
    __tablename__ = 'RepaymentHistory'

    repayment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    repayment_date = db.Column(db.Date, nullable=False)
    repayment_amount = db.Column(db.Integer, nullable=False)
    remaining_balance = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "repayment_id": self.repayment_id,
            "user_id": self.user_id,
            "repayment_date": self.repayment_date,
            "repayment_amount": self.repayment_amount,
            "remaining_balance": self.remaining_balance,
            "description": self.description
        }


class Transactions(db.Model):
    __tablename__ = 'Transactions'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id', ondelete="CASCADE"), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    payment_method = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "transaction_date": self.transaction_date.strftime('%Y-%m-%d') if self.transaction_date else None,
            "amount": self.amount,
            "description": self.description,
            "payment_method": self.payment_method
        }



# Notification 테이블
class Notification(db.Model):
    __tablename__ = 'Notification'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "sent_at": self.sent_at
        }
