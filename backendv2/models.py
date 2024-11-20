from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Table, Float, TIMESTAMP, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    monthly_income = Column(Integer, nullable=False)
    monthly_expense = Column(Integer, nullable=False)
    available_funds = Column(Integer, nullable=False)  # MySQL에선 GENERATED ALWAYS AS 지원 필요
    loan_amount = Column(Integer, nullable=False)
    interest_rate = Column(Float, nullable=False)
    repayment_period = Column(Integer, nullable=False)
    monthly_repayment_goal = Column(Integer, nullable=False)
    selected_plan_group_id = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # transactions = relationship("Transactions", back_populates="user")

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


class Categories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)

    # transactions = relationship("Transactions", back_populates="category")


class Transactions(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id', ondelete="CASCADE"), nullable=False)
    transaction_date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    payment_method = Column(String(255), nullable=True)

    # Relationships
    # user = relationship("User", backref="transactions")
    # category = relationship("Categories", backref="transactions")

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "transaction_date": self.transaction_date.strftime('%Y-%m-%d') if self.transaction_date else None,
            "amount": self.amount,
            "description": self.description,
            "payment_method": self.payment_method,
            "category_name": self.category.category_name if self.category else None,
            "user_name": self.user.name if self.user else None
        }


# RepaymentHistory 테이블
class RepaymentHistory(Base):
    __tablename__ = 'repaymentHistory'

    repayment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    repayment_date = Column(Date, nullable=False)
    repayment_amount = Column(Integer, nullable=False)
    remaining_balance = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "repayment_id": self.repayment_id,
            "user_id": self.user_id,
            "repayment_date": self.repayment_date,
            "repayment_amount": self.repayment_amount,
            "remaining_balance": self.remaining_balance,
            "description": self.description
        }

# RepaymentPlans 테이블
class RepaymentPlans(Base):
    __tablename__ = 'repaymentPlans'

    plan_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    plan_name = Column(Text, nullable=False)
    total_amount = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    details = Column(JSON, nullable=False)
    hashtags = Column(Text, nullable=False)  # hashtags 필드 추가
    created_at = Column(TIMESTAMP, nullable=False)

    def to_dict(self):
        return {
            "plan_id": self.plan_id,
            "user_id": self.user_id,
            "plan_name": self.plan_name,
            "total_amount": self.total_amount,
            "duration": self.duration,
            "details": self.details,
            "hashtags": self.hashtags,  # to_dict에 hashtags 포함
            "created_at": self.created_at
        }

# UserExpenses 테이블
class UserExpenses(Base):
    __tablename__ = 'userExpenses'
    user_expense_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    original_amount = Column(Integer, nullable=False)
    is_hard_to_reduce = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "user_expense_id": self.user_expense_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "month": self.month,
            "original_amount": self.original_amount,
            "is_hard_to_reduce": self.is_hard_to_reduce
        }

# Notification 테이블
class Notification(Base):
    __tablename__ = 'notification'

    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "sent_at": self.sent_at
        }
