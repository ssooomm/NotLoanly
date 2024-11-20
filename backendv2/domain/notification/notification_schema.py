from pydantic import BaseModel
from typing import List, Optional

class TransactionCreate(BaseModel):
    user_id: int
    category_id: int
    transaction_date: str
    amount: float
    description: Optional[str] = None
    payment_method: Optional[str] = None

class TransactionResponse(BaseModel):
    message: str

class NotificationResponse(BaseModel):
    notification_id: int
    message: str
    sent_at: str

class NotificationsListResponse(BaseModel):
    status: str
    notifications: List[NotificationResponse]