from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from database import SessionLocal
from domain.notification.notification_crud import TransactionCRUD


def send_repayment_reminders():
    """
    하루 전 상환일 알림을 전송합니다.
    """
    db: Session = SessionLocal()
    try:
        notification_crud = TransactionCRUD(db)
        result = notification_crud.send_repayment_reminder_notifications()
        print(result)  # 로그 출력
    except Exception as e:
        print(f"Error sending repayment reminders: {e}")
    finally:
        db.close()


def start_notification_scheduler():
    """
    스케줄러를 시작하고 알림 관련 작업을 예약합니다.
    """
    scheduler = BackgroundScheduler()
    #scheduler.add_job(send_repayment_reminders, "cron", hour=10)  # 매일 오전 10시 실행
    scheduler.add_job(send_repayment_reminders, "cron", hour=23, minute=31)  # 매일 오전 10시 실행

    scheduler.start()
    print("Notification scheduler started!")
