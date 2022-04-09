from django.db import transaction
from rest_framework_simplejwt import tokens

from shigoto_q.users.models import Subscriber


def create_subscriber(data):
    print(data)
    subscriber = Subscriber.objects.create(**data)
    return subscriber.__dict__


def blacklist_token(payload):
    with transaction.atomic():
        tokens.RefreshToken(payload.get("refresh_token")).blacklist()
