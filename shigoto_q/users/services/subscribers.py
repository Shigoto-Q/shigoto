import logging

from django.db import transaction
from rest_framework_simplejwt import tokens

from shigoto_q.emails.services import send_email
from shigoto_q.emails.constants import EmailTypes, EmailPriority
from shigoto_q.users.models import Subscriber
from shigoto_q.users.metrics import metrics


_LOG_PREFIX = "[SUBSCRIBER-SERVICES]"
logger = logging.getLogger(__name__)


def create_subscriber(data):
    metrics.incr("new.subscriber.count")
    logger.info(f"{_LOG_PREFIX} Creating new subscriber({data}).")
    subscriber = Subscriber.objects.create(**data)
    send_email(
        template_name=EmailTypes.USER_SUBSCRIPTION,
        priority=EmailPriority.HIGH,
        override_email=subscriber.email,
        context={},
    )
    return subscriber.__dict__


def remove_subscriber(email):
    logger.info(f"{_LOG_PREFIX} Deleting subscriber.")
    Subscriber.objects.filter(email=email).delete()


def blacklist_token(payload):
    with transaction.atomic():
        tokens.RefreshToken(payload.get("refresh_token")).blacklist()
