import logging

from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from shigoto_q.users.services import customers as customer_services


logger = logging.getLogger(__name__)
_LOG_PREFIX = "[USER-SERVICE]"

User = get_user_model()


def get_user(pk):
    # TODO Add minute=0
    strip_date = dict(second=0, microsecond=0)
    user = User.objects.get(pk=pk)
    is_first_login = user.date_joined.replace(**strip_date) == user.last_login.replace(
        **strip_date
    )
    user_data = dict(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        two_factor_auth_enabled=user.two_factor_auth_enabled,
        is_first_login=is_first_login,
    )
    return user_data


@transaction.atomic()
def create_user(data):
    data["password"] = make_password(data["password"])

    user = User.objects.create(**data)
    customer = customer_services.create_customer(
        name=user.full_name,
        email=user.email,
    )
    user.customer = customer
    user.save()
    logger.info(f"{_LOG_PREFIX} Creating User(id={user.id}, email={user.email})")
    return user.__dict__


def list_users(filters=None):
    filters = filters or {}
    return User.objects.filter(**filters)
