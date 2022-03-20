import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

logger = logging.getLogger(__name__)
_LOG_PREFIX = "[USER-SERVICE]"

User = get_user_model()


def get_user(pk):
    return User.objects.get(pk=pk).__dict__


def create_user(data):
    data["password"] = make_password(data["password"])

    user = User.objects.create(**data)
    logger.info(f"{_LOG_PREFIX} Creating User(id={user.id}, email={user.email})")
    return user.__dict__


def list_users(filters):
    return list(User.objects.filter(**filters).values())
