import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("shigoto_q")

app.conf.update(
    result_backend="django-db",
)
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     "send-queued-mail": {
#         "task": "post_office.tasks.send_queued_mail",
#         "schedule": 600.0,
#     },
# }
