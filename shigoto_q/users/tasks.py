from django.contrib.auth import get_user_model
import time
from config import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task(track_started=True)
def tst_task():
    time.sleep(5)
