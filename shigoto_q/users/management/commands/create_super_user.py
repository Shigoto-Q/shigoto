from __future__ import absolute_import

import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


logger = logging.getLogger(__name__)
_LOG_PREFIX = "[CREATE-SUPER-USER]"


class Command(BaseCommand):
    help = "Generate dummy users"

    def add_arguments(self, parser):
        parser.add_argument("-n", "--name", type=str, help="First and last name")
        parser.add_argument("-e", "--email", type=str, help="User email")

    def handle(self, *args, **options):
        first_name, last_name = options.get("name").split(" ")
        email = options.get("email")

        if settings.DEBUG:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_staff=True,
            )
            user.set_password('123')
            user.save()
            logger.info(
                f"{_LOG_PREFIX} Creating User(first_name={first_name}, last_name={last_name}, email={email})."
            )
