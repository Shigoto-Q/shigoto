from __future__ import absolute_import

from django.core.management.base import BaseCommand
from django.db import transaction

from shigoto_q.users import models as user_models
from tests.factory.users import users_factory


class Command(BaseCommand):
    help = "Generate dummy users"
    _number_of_users = 20
    _number_of_admins = 2
    _password = users_factory.UserFactory.password

    @transaction.atomic
    def _create_normal_users(self):
        self.stdout.write("Generating new users...")
        users = []
        for _ in range(self._number_of_users):
            user = users_factory.UserFactory()
            self.stdout.write(
                f"Creating User(id={user.id}, username={user.username}, password={self._password})"
            )
            users.append(user)
            user.save()
        self.stdout.write(f"Successfully created {len(users)} normal users.")

    @transaction.atomic
    def _create_super_users(self):
        admins = []
        for _ in range(self._number_of_admins):
            admin = users_factory.UserFactory(flag_is_superuser=True)
            self.stdout.write(
                f"Creating User(id={admin.id}, username={admin.username}, password={self._password})"
            )
            admins.append(admin)
            admin.save()
        self.stdout.write(f"Successfully created {len(admins)} superusers.")

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        user_models.User.objects.all().delete()
        self._create_normal_users()
        self._create_super_users()
