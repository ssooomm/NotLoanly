# from fastapi import HTTPException

# from domain.notification.notification_schema import *
# from models import Transactions, Notification

# from sqlalchemy.orm import Session
# from sqlalchemy import func

# def create_transaction(self, transaction: TransactionCreate) -> bool:
#     try:
#         db_transaction = Transactions(
#             user_id=transaction.user_id,
#             category_id=transaction.category_id,
#             transaction_date=transaction.transaction_date,
#             amount=transaction.amount,
#             description=transaction.description,
#             payment_method=transaction.payment_method
#         )
#         self.db.add(db_transaction)
#         self.db.commit()
#         self.db.refresh(db_transaction)
#         return True
#     except Exception as e:
#         self.db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import HTTPException
from sqlalchemy.orm import Session
from domain.notification.notification_schema import TransactionCreate
from models import Transactions, Notification


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
