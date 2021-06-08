import time

from django.contrib.auth import get_user_model

from config import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task(track_started=True)
def tst_task():
    time.sleep(5)


class Yea(object):

    """Docstring for Yea. """

    def __init__(self):
        """TODO: to be defined. """
        s
