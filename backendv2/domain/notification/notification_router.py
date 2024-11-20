from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List, Any

from database import get_db
from domain.notification import notification_crud, notification_schema

router = APIRouter(
    prefix="/api/notification",
)


@router.post("/transactions", response_model=notification_schema.TransactionResponse, status_code=201)
async def create_transaction(
        transaction: notification_schema.TransactionCreate,
        db: Session = Depends(get_db)
) -> Any:
    transaction_crud = notification_crud.TransactionCRUD(db)
    if transaction_crud.create_transaction(transaction):
        return {"message": "Transaction created successfully"}


@router.get("/notifications/{user_id}", response_model=notification_crud.NotificationsListResponse)
async def get_notifications(
        user_id: int,
        db: Session = Depends(get_db)
) -> Any:
    notification_crud = notification_schema.NotificationCRUD(db)
    notifications = notification_crud.get_user_notifications(user_id)

    return {
        "status": "success",
        "notifications": notifications
    }