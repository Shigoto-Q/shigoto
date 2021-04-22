from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import PeriodicTask, CrontabSchedule


class User(AbstractUser):
    first_name = models.CharField(max_length=256, default="")
    last_name = models.CharField(max_length=256, default="")
    company = models.CharField(max_length=100, default="")
    customer = models.ForeignKey(
        "djstripe.Customer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Stripe Customer Object"),
    )
    subscription = models.ForeignKey(
        "djstripe.Subscription",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Stripe Subscripton Object"),
    )
    total_tasks = models.IntegerField(default=0)
    crontab = models.ManyToManyField(CrontabSchedule)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserTasks(models.Model):
    task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE)
