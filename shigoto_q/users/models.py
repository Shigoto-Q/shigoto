from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask


class User(AbstractUser):
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    total_tasks = models.IntegerField(default=0)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserTasks(models.Model):
    task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)
