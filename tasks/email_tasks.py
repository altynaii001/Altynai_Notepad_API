import time
from celery_app import celery_app

@celery_app.task
def mock_email(email: str):
    time.sleep(10)
    print(f"Email sent to {email}")