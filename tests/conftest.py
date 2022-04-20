import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factory.users import users_factory
from tests.factory.schedule import schedule_factory


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": "redis://", "result_backend": "redis://"}


@pytest.fixture
def regular_user():
    u = users_factory.UserFactory()
    u.save()
    return u


@pytest.fixture
def admin_user():
    return users_factory.UserFactory(flag_is_superuser=True)


@pytest.fixture
def regular_client(regular_user):
    c = APIClient()
    refresh = RefreshToken.for_user(regular_user)
    c.credentials(HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token))
    return c


@pytest.fixture
def interval_schedule():
    inter = schedule_factory.IntervalFactory()
    inter.save()
    return inter
