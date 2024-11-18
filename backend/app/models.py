from . import db

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
    
class Categories(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)
    

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


class Categories(db.Model):
    __tablename__ = 'Categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)
