from fastapi import HTTPException

from domain.notification.notification_schema import *
from models import Transactions, Notification

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
        raise HTTPException(status_code=500, detail=str(e))
