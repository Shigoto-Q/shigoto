import pytest

from tests.factory.users import users_factory


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": "redis://", "result_backend": "redis://"}


@pytest.fixture
def regular_user():
    return users_factory.UserFactory()
