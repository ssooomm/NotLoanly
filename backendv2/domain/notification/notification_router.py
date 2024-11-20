from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from database import get_db
from domain.notification import notification_schema, notification_crud

from fastapi.responses import StreamingResponse
import asyncio
from shared_memory import notifications  # 공유 메모리 임포트

import json

router = APIRouter(
    prefix="/api/notification",
    tags=["notifications"]
)


@router.post("/transactions", response_model=notification_schema.TransactionResponse, status_code=201)
async def create_transaction(
        transaction: notification_schema.TransactionCreate,
        db: Session = Depends(get_db)
) -> Any:
    transaction_service = notification_crud.TransactionCRUD(db)
    if transaction_service.create_transaction(transaction):
        return {"message": "Transaction created successfully"}
    raise HTTPException(status_code=500, detail="Failed to create transaction")


@router.get("/notifications/{user_id}", response_model=notification_schema.NotificationsListResponse)
async def get_notifications(
        user_id: int,
        db: Session = Depends(get_db)
) -> Any:
    notification_service = notification_crud.TransactionCRUD(db)
    notifications = notification_service.get_user_notifications(user_id)
    return {
        "status": "success",
        "notifications": notifications
    }



async def notification_event_generator(user_id: int):
    try:
        while True:
            if len(notifications) > 0:
                # 사용자 ID로 필터링된 메시지
                filtered_notifications = [msg for msg in notifications if msg.get("user_id") == user_id]
                for notification in filtered_notifications:
                    print(f"Sending message to user {user_id}: {notification['message']}")  # 디버깅 로그
                    # JSON 형식으로 직렬화하여 스트림 전송
                    yield f"data: {json.dumps(notification)}\n\n"
                    notifications.remove(notification)  # 큐에서 제거
            await asyncio.sleep(1)  # 1초마다 확인
    except Exception as e:
        print(f"Error in notification_event_generator: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@router.get("/stream/{user_id}", response_class=StreamingResponse)
async def notification_stream(user_id: int):
    """
    사용자별 알림 스트림을 위한 SSE 엔드포인트
    """
    try:
        return StreamingResponse(notification_event_generator(user_id), media_type="text/event-stream")
    except Exception as e:
        print(f"Error in notification_stream: {e}")
        raise HTTPException(status_code=500, detail="Stream error")
